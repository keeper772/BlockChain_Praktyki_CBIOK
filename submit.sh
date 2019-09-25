#delete previous output files
rm miner.log miner.out
#submiting jobs
condor_submit miner.submit
#wait until at least one miner ends job
condor_wait -num 1 miner.log

