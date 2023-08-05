"""没有改进的原始版wdl-rf
去掉标准化
训练并保存模型和权重值
"""
import pickle
import autograd.numpy.random as npr
from autograd import grad
from wdl.util import load_data
from wdl.build_wdl_fp_v0 import build_wdl_fingerprint_fun,build_wdl_deep_net
from wdl.optimizers import adam
from wdl.util import build_batched_grad
from wdl.util import rmse, Rs2
from sklearn.ensemble import RandomForestRegressor

from wdl.run_utils import file_split2
from wdl.run_utils import InitParam
from wdl.run_utils import save_experiment

def train_nn(pred_fun, loss_fun, num_weights, train_smiles, train_raw_targets, train_params, seed=0,
             validation_smiles=None, validation_raw_targets=None):
    """loss_fun has inputs (weights, smiles, targets)"""
    print("Total number of weights in the network:", num_weights)
    init_weights = npr.RandomState(seed).randn(num_weights) * train_params['init_scale']
    train_targets = train_raw_targets
    training_curve = []

    def callback(weights, iter):
        if iter % 10 == 0:
            print("----------")
            #print("max of weights", np.max(np.abs(weights)))
            train_preds = pred_fun(weights,train_smiles)
            cur_loss = loss_fun(weights, train_smiles, train_targets)
            training_curve.append(cur_loss)
            print("Iteration", iter, "loss", cur_loss)
            print("train RMSE", rmse(train_preds, train_raw_targets))
            print("train R^2", Rs2(train_preds, train_raw_targets))
            if validation_smiles is not None:
                validation_preds = pred_fun(weights, validation_smiles)
                print("Validation RMSE", iter, ":", rmse(validation_preds, validation_raw_targets))
                print("Validation R^2", iter, ":", Rs2(validation_preds, validation_raw_targets))

    # Build gradient using autograd.
    grad_fun = grad(loss_fun)
    grad_fun_with_data = build_batched_grad(grad_fun, train_params['batch_size'],
                                            train_smiles, train_targets)

    # Optimize weights.
    trained_weights = adam(grad_fun_with_data, init_weights, callback=callback,
                           num_iters=train_params['num_iters'], step_size=train_params['step_size'])

    def predict_func(new_smiles):
        """Returns to the original units that the raw targets were in."""
        return pred_fun(trained_weights, new_smiles)

    return predict_func, trained_weights, training_curve


def run_experiment(param):
    """
    根据输入的数据训练wdl_rf模型
    :param param: InitParam类对象,初始化时传入要训练的csv文件,wdl网络的两个重要参数：迭代次数和batch_size
                                    调用save_model方法保存模型
    :return:
    """
    print("Loading data...")
    task_params = param.file_params
    model_params = param.model_params
    train_params = param.train_params
    vanilla_net_params = param.vanilla_net_params
    save_params = param.save_params

    traindata, testdata = load_data(
        task_params['input_file'], file_split2(task_params['input_file']),
        input_name='smiles', target_name=task_params['target_name'])
    train_inputs, train_targets = traindata
    val_inputs, val_targets = testdata
    test_inputs, test_targets = testdata

    def build_single_weight_fp_experiment(init_weights, x=0):
        fp_depth = x
        hidden_layer_sizes = [model_params['hidden_width']] * fp_depth
        hidden_arch_params = {'num_hidden_features': hidden_layer_sizes,
                              'fp_length': model_params['fp_length'], 'normalize': 1}
        fp_func, conv_parser = build_wdl_fingerprint_fun(**hidden_arch_params)
        trainfp = fp_func(init_weights, train_inputs)
        testfp = fp_func(init_weights, test_inputs)
        return trainfp, testfp

    def build_weight_fp_experiment(init_weight):
        train_x0, test_x0 = build_single_weight_fp_experiment(init_weight, 0)
        train_x = model_params['layer_weight'] * train_x0
        test_x = model_params['layer_weight'] * test_x0
        for i in range(1, model_params['fp_depth']):
            train_x1, test_x1 = build_single_weight_fp_experiment(init_weight, i)
            train_x = train_x + model_params['layer_weight'] * (train_x1 - train_x0)
            test_x = test_x + model_params['layer_weight'] * (test_x1 - test_x0)
            train_x0 = train_x1
            test_x0 = test_x1
        train_xx, test_xx = build_single_weight_fp_experiment(init_weight, model_params['fp_depth'])
        train_x = train_x + train_xx - train_x0
        test_x = test_x + test_xx - test_x0
        return train_x, test_x

    def run_weight_fp_experiment():
        hidden_layer_sizes = [model_params['hidden_width']] * model_params['fp_depth']
        hidden_arch_params = {'num_hidden_features': hidden_layer_sizes,
                              'fp_length': model_params['fp_length'], 'normalize': 1}
        loss_fun, pred_fun, wfp_parser = \
            build_wdl_deep_net(hidden_arch_params, vanilla_net_params, model_params['L2_reg'])
        num_weights = len(wfp_parser)
        predict_func, trained_weights, conv_training_curve = \
            train_nn(pred_fun, loss_fun, num_weights, train_inputs, train_targets,
                     train_params, validation_smiles=val_inputs, validation_raw_targets=val_targets)
        return trained_weights

    print("Task params", task_params)
    print(file_split2(task_params['input_file']))
    print("Starting weight fingerprint experiment...")
    trained_weights = run_weight_fp_experiment()
    train_x, test_x = build_weight_fp_experiment(trained_weights)
    if(save_params['flag']):
        with open(save_params['weights_file'], 'wb') as weights_file:
            pickle.dump(trained_weights, weights_file)
    train_y = train_targets


    clf = RandomForestRegressor(model_params['n_estimators'], max_features='log2')#sqrt
    clf = clf.fit(train_x, train_y)
    if(save_params['flag']):
        with open(save_params['model_file'], 'wb') as fw:
            pickle.dump(clf, fw)

    print('-----------------------pip version-------------------------')
    print("input_file:",param.file_params['input_file'])
    print("num_iters:", param.train_params["num_iters"])
    print("batch_size:", param.train_params["batch_size"])
    RMSE = rmse(clf.predict(test_x), test_targets)
    r2 = Rs2(clf.predict(test_x), test_targets)
    print("WDL_RF test RMSE:", RMSE,"\t test R2:", r2)
    if(param.save_params['flag']):
        """保存最终模型"""
        print("savemodel:",param.save_params)

    """记录训练过程中调参的结果"""
    save_experiment(param.record_file, param.file_params['input_file'],
            param.train_params["num_iters"], param.train_params["batch_size"], RMSE, r2)


if __name__ == '__main__':
    #param = InitParam("E:\keti_data\A1.csv", 200, 20)
    #param.save_record("record.csv")
    #param.save_model("E:\\wdl_rf_package\\wdl_rf\\model\\A1_trained_weights.pkl", "E:\\wdl_rf_package\\wdl_rf\\model\\A1_RF.pkl")
    #run_experiment(param)