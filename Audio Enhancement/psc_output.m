function output = psc_output(filename)

[x, fs] = audioread(filename);
outputPSC = psc( x, fs, 25, 25/2, 'Griffin & Lim', 3.74 );
filename_output='outputPSC.wav';
audiowrite(filename_output,outputPSC,fs);

output = filename_output;