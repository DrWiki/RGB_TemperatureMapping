clear;
close all;

col = 951;
row = 604;

Tem_range = 15:39;

for Tem = Tem_range
    filename = ['.\pic\', num2str(Tem), '.jpg'];
    I = imread(filename);
    I(row-1:row+1, col-1:col+1, :) = 255;

    figure;
    imshow(I);
    hold on

    title(num2str(Tem));

end
