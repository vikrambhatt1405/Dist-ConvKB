# Dist-ConvKB
## Machine Learning with Large Datasets
```
python stale_sync.py --embedding_dim 100 --num_filters 50 --learning_rate 0.000005 --name FB15k-237 --useConstantInit --model_name fb15k237 --ps_hosts=10.24.1.219:2000 --worker_hosts=10.24.1.220:2001,10.24.1.221:2002,10.24.1.222;2003,10.24.1.223:2004, --job_name=ps --task_index=0 
```


```
python downpour_train.py --embedding_dim 100 --num_filters 50 --learning_rate 0.000005 --name FB15k-237 --useConstantInit --model_name fb15k237 --ps_hosts=10.24.1.219:2000 --worker_hosts=10.24.1.220:2001,10.24.1.221:2002,10.24.1.222:2003,10.24.1.223:2004,10.24.1.224:2005 --job_name=ps --task_index=0
```
```
 python async_train.py --embedding_dim 100 --num_filters 50 --learning_rate 0.000005 --name FB15k-237 --useConstantInit --model_name fb15k237 --ps_hosts=10.24.1.218:2000 --worker_hosts=10.24.1.219:2001,10.24.1.220:2002 --job_name=worker --task_index=0
```
```
 python async_train.py --embedding_dim 100 --num_filters 50 --learning_rate 0.000005 --name FB15k-237 --useConstantInit --model_name fb15k237 --ps_hosts=10.24.1.218:2000 --worker_hosts=10.24.1.219:2001,10.24.1.220:2002 --job_name=worker --task_index=0
 ```
**Freebase/** folder contains Hadoop mapreduce job written for pre-processing entire freebase data dump which outputs hdfs file of 17GB.
