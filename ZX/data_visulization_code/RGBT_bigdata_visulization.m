% 将数据可视化
clear
clc
close all

maxbias = 20;
% 输出文件名
res_filename = ['.\T_RGB_avg_var_maxbias', num2str(maxbias), '.csv'];

Tem_range = 15:39;
% 每个数据441行

row_of_1degree = (maxbias*2+1)^2;
row_end = (39-15+1) * row_of_1degree + 1;
%% 渐变色表
R_color = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, ...
	240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0, ...
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...
	0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240 ];

G_color = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...
	0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, ...
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, ...
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255 ];

B_color = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, ...
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, ...
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, ...
	240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0, ...
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];


%% 读取数据
RGBT_data = csvread('..\data\EveryDegree\RGBT_with_all_T_step1_maxbias20.csv', 1, 0);
R = RGBT_data(:, 1);
G = RGBT_data(:, 2);
B = RGBT_data(:, 3);
T = RGBT_data(:, 4);

% 方差
var_R = zeros(size(Tem_range))';
var_G = var_R;
var_B = var_R;

% 均值
avg_R = zeros(size(Tem_range))';
avg_G = avg_R;
avg_B = avg_R;

Tem = 15;   % 初始温度

%% 求均值、方差，画大数据分布图
figure
hold on
for ii = 1:row_of_1degree:row_end-1
    index = floor(ii/row_of_1degree) + 1;   % 对应记录向量的坐标
    
    % 方差
    var_R(index) = var(R(ii : ii+row_of_1degree-1));
    var_G(index) = var(G(ii : ii+row_of_1degree-1));
    var_B(index) = var(B(ii : ii+row_of_1degree-1));
    
    % 均值
    avg_R(index) = mean(R(ii : ii+row_of_1degree-1));
    avg_G(index) = mean(G(ii : ii+row_of_1degree-1));
    avg_B(index) = mean(B(ii : ii+row_of_1degree-1));
    
    % 画图
    color_index = round(65-2.65*(index-1));  % 色谱的index

    scatter3(R(ii : ii+row_of_1degree-1) , G(ii : ii+row_of_1degree-1), ...
        B(ii : ii+row_of_1degree-1), 30, ...
        [R_color(color_index),G_color(color_index), B_color(color_index)]/255, '.');
    text(avg_R(index), avg_G(index), avg_B(index), num2str(Tem), ...
        FontSize=12, FontWeight="bold");
    
    % 温度升高1°C
    Tem = Tem + 1;
end

xlabel('R');
ylabel('G');
zlabel('B');
title('各个温度点的RGB值')
box on
grid on
legend('15°C', '16°C', '17°C', '18°C', '19°C', '20°C',...
       '21°C', '22°C', '23°C', '24°C', '25°C', '26°C', '27°C', '28°C', '29°C', '30°C',...
       '31°C', '32°C', '33°C', '34°C', '35°C', '36°C', '37°C', '38°C', '39°C',...
       'NumColumnsMode', 'manual', 'NumColumns', 3);
view([40 35]);
set(gca,'FontSize', 15);
%% 输出到表格
% % 合并成矩阵
% T_RGB_avg_var_record = [Tem_range', avg_R, avg_G, avg_B...
%     var_R, var_G, var_B];   % 合并成矩阵
% 
% % 写入csv文件
% writematrix(T_RGB_avg_var_record, res_filename, 'WriteMode', 'overwrite');