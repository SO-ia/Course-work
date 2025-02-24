function output = NSSP_output(filename)

[x, fs] = audioread(filename);
outputNSSP = NSSP(x, fs);
filename_output = 'outputNSSP.wav';
audiowrite(filename_output, outputNSSP, fs);

output = filename_output;
