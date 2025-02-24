function output = mss_smpo_output(filename)

[x, fs] = audioread(filename);
mss_smpo(filename,'smpo_xre.wav');
outputSMPO=audioread('smpo_xre.wav');
filename_output='outputSMPO.wav';
audiowrite(filename_output,outputSMPO,fs);

output = filename_output;