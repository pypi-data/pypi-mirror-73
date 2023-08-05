import csv

import numpy
from wdl.util import rmse

def file_split(filename):
    """
    将数据集切分为训练集、验证集、测试集
    :param filename:
    :return:
    """
    with open(filename,'r') as f:
        num = len(f.readlines())-1
    N_val = int(round(num/5.0))
    N_test = int(round(num/5.0))
    N_train = num - N_val- N_test
    return (N_train,N_val,N_test)

def file_split2(filename):
    """
    将数据集按3：1切分为训练集、测试集
    :param filename:
    :return:（训练集的个数，测试集的个数）
    """
    with open(filename,'r') as f:
        num = len(f.readlines())-1
    N_test = int(round(num/4.0))
    N_train = num - N_test
    return (N_train,N_test)

def save_experiment(filename,c1,c2,c3,c4,c5):
    """
    记录训练的结果
    :param filename: 保存的文件
    :param c1: input_File
    :param c2: num_iters
    :param c3: batch_size
    :param c4: RMSE
    :param c5: R2
    :return:
    """
    with open(filename,'a',newline='') as fw:
        writer = csv.writer(fw)
        writer.writerow([c1,c2,c3,c4,c5])

def read_csv(filename):
    """从输入的文件中获取smiles分子式,输入文件的第一行是列名"""
    with open(filename,'r') as fr:
        lines = csv.reader(fr)
        if (len(fr.readline()) > 10):
            #输入文件是原始的跑数据用的数据集
            res = [l[2] for l in lines]
        else:
            # 自己输入的只有一列的smiles分子式
            res = [l for l in lines]
    return res

def write_csv(filename,data):
    """将结果data存到filename文件中"""
    with open(filename,'w',newline='') as fw:
        writer = csv.writer(fw)
        for i in data:
            writer.writerow([i])

def addwrite_csv(inputfile,outputfile,data,column_name):
    """
    保存结果
    :param inputfile: 原始输入的待预测配体分子的文件，作为保存结果文件的模板
    :param outputfile: 输出结果所保存的文件
    :param data: 预测得到的结果
    :param column_name: 保存文件中当前列的列名
    :return:
    """
    print('得出',column_name,'存放在',outputfile)
    with open(inputfile,'r') as fr:
        lines = csv.reader(fr)
        with open(outputfile,'w',newline='') as fw:
            writer = csv.writer(fw)
            i = 0
            for l in lines:
                if i==0:
                    l.append(column_name)
                    writer.writerow(l)
                else:
                    l.append(data[i-1])
                    writer.writerow(l)
                i+=1

def addwrite_csv2(inputfile,outputfile,pvalue,fp):
    """
    保存预测得到的活性和分子指纹,文件第一行都是列名
    :param inputfile: 原始输入的待预测配体分子的文件
    :param outputfile: 输出结果所保存的文件
    :param pvalue: 预测得到的配体分子与gpce的结合活性
    :param fp: 生成的分子指纹
    :return:
    """
    print('输出的分子指纹和生物活性所保存的文件：',outputfile)
    with open(inputfile,'r') as fr:
        lines = csv.reader(fr)
        with open(outputfile,'w',newline='') as fw:
            writer = csv.writer(fw)
            i = 0
            for l in lines:
                if i==0:
                    l.append('predict_value')
                    l.append('fp')
                    writer.writerow(l)
                else:
                    l.extend([pvalue[i-1],fp[i-1]])
                    writer.writerow(l)
                i+=1


class InitParam():
    """训练所需要的参数类"""
    file_params = {'target_name': 'STANDARD_VALUE',
              'input_file': 'E:\keti_data\A1.csv', }

    train_params = dict(num_iters=200,
                        batch_size=5,
                        init_scale=numpy.exp(-4),
                        step_size=0.01)

    model_params = dict(fp_length=50,
                        fp_depth=4,
                        hidden_width=20,
                        h1_size=100,
                        layer_weight=0.5,
                        n_estimators=100,
                        max_features='sqrt',
                        L2_reg=numpy.exp(-2))
    vanilla_net_params = dict(
        layer_sizes=[model_params['fp_length'], model_params['h1_size']],
        normalize=True, L2_reg=model_params['L2_reg'], nll_func=rmse)

    save_params = dict(flag=False,weights_file="weights.pkl",model_file="model.pkl")

    def __init__(self,filename, n_iters, batch_size):
        self.file_params['input_file'] = filename
        self.train_params['num_iters'] = n_iters
        self.train_params['batch_size'] = batch_size

    def save_model(self,weights_file,model_file):
        """
        将训练出来的模型保存到相应的文件中
        :param weights_file: wdl部分的权重
        :param model_file: rf模型
        :return:
        """
        self.save_params['flag'] = True
        self.save_params['weights_file'] = weights_file
        self.save_params['model_file'] = model_file


if __name__ == "__main__":
    print(InitParam.file_params['input_file'].split('\\')[-1].split('.')[0]+'.pkl')
    #save_experiment('result\\experiment_record.csv',"input_file","num_iters","batch_size","RMSE","R2")
    #param = InitParam("E:\keti_data\A1new.csv",200,5)
    #print(param.file_params)
    #write_csv('test.csv',[-0.30537,-2.79966,-3.1034])
    #print(res)