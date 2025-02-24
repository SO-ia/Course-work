function output = SSMultibandKamath02_output(filename)

[x, fs] = audioread(filename);
outputKamath=SSMultibandKamath02(x,fs);
filename_output='outputKamath.wav';
audiowrite(filename_output,outputKamath,fs);

output = filename_output;