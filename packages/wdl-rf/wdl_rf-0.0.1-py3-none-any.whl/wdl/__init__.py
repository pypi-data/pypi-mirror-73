"""from wdl.util import tictoc, normalize_array, WeightsParser, build_batched_grad, add_dropout,\
     get_output_file, get_data_file, load_data, load_data_slices, output_dir,load_data1,load_data2,wdl_lose_fun
#from wdl.optimizers import adam
#from wdl.rdkit_utils import smiles_to_fps,smiles_to_fps1
from wdl.build_wdl_fp_v0 import build_wdl_deep_net, build_wdl_fingerprint_fun,array_rep_from_smiles
from wdl.build_wdl_net_v0 import build_morgan_deep_net, build_morgan_fingerprint_fun, \
     build_standard_net, binary_classification_nll, mean_squared_error, relu, \
     build_mean_predictor, categorical_nll,build_maccs_deep_net,build_maccs_fingerprint_fun,\
     build_FCFP_fingerprint_fun,build_FCFP_deep_net
from wdl.mol_graph import degrees,graph_from_smiles_tuple
from wdl.features import atom_features,num_bond_features,num_atom_features"""

from wdl.run_utils import addwrite_csv2,addwrite_csv,write_csv,read_csv
from wdl.demo_predict import predict_fp_and_pvalue
from wdl.demo_train import run_experiment,InitParam

