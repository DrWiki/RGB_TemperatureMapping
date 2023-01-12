%% 数据格式说明
% 前三列分别为R G B，范围为[0, 255]。（python转换的时候要注意BGR）
% 第四列为T/摄氏度
clear
clc
close all
disp('--------------------get RGB program begin (use data)--------------------')
%% 参数选择
Tem_range = 15:39;  % 温度范围

% 中心点偏离度设置
max_bias = 15;  % 最大偏离度
step = 1;       % 步长

res_filename = ['..\data\EveryDegree\RGBT_with_all_T_step',num2str(step),...
    '_maxbias', num2str(max_bias), '.csv'];    % 输出的表格名称
for Tem = Tem_range
    % num = 1:length(Tem_range)'; % 输出时的表格编号
    
    sz = 9;     % 滤波窗的大小
    RGBT_rc_data = csvread('..\data\RGBT_rc_record.csv');
    row_center_data = RGBT_rc_data(:, 5);
    col_center_data = RGBT_rc_data(:, 6);
    
    row_center = row_center_data(Tem-14);
    col_center = col_center_data(Tem-14);
    %% 图像读取与滤波
    filename = ['..\pic\', num2str(Tem), '.jpg'];
    I0 = imread(filename);     % 选择文件，读取原图
    
    % 提取三个通道的颜色，准备进行均值滤波
    R_I0 = I0(:, :, 1);
    G_I0 = I0(:, :, 2);
    B_I0 = I0(:, :, 3);
    
    %     % 展示原图
    %     figure
    %     imshow(I0);
    %     title(['T = ', num2str(Tem), '°C', '(Origin)'])
    
    % 滤波
    % 通常情况下，均值滤波和中值滤波针对的是二维图像，
    % 如果是彩色图像需转化为灰度图像进行滤波。
    % 除此之外，也可以对彩色图像的三个通道分别进行滤波，最后再合并即可。
    win = [sz sz]; 
    h = fspecial('average', win); % 均值滤波器
    
    % 分三个通道进行均值滤波
    R_I = filter2(h, R_I0);
    G_I = filter2(h, G_I0);
    B_I = filter2(h, B_I0);
    
    % 合并
    I = cat(3, R_I, G_I, B_I);
    I = uint8(I);
    
    %     % 展示滤波后的图
    %     figure
    %     imshow(I);
    %     title(['T = ', num2str(Tem), '°C', '(Average Filter)'])
    %% 使用矩阵算法采集数据
    % 设置偏移的范围，对图像进行分析可知，bias <= 30都可信，<=20绝对稳
    row_b_range = -max_bias:step:max_bias;
    col_b_range = -max_bias:step:max_bias;
    
    
    %% 本次的采样点坐标 = 中心点坐标 + 偏移量
    row_v = row_center + row_b_range;
    col_v = col_center + col_b_range;
    
    %% 提取RGB值
    
    % 记录到RGB矩阵中
    R = I(row_v, col_v, 1);
    G = I(row_v, col_v, 2);
    B = I(row_v, col_v, 3);
    
    % 记录coly坐标值到向量中，i.e.记录选取点
    %     col_v(Tem-14) = col;
    %     row_v(Tem-14) = row;
    
    %     disp(['RGB值：[', num2str(R(Tem-14)), ', ' num2str(G(Tem-14)), ...
    %         ', ' num2str(B(Tem-14)) ']'])
    %     disp('------------------------------')
    
    % 拉成列向量
    R = R(:);
    B = B(:);
    G = G(:);
    %% 合并矩阵，写入到表格中
    RGBT_record = 0; % 先清空为0
    Tem_v = Tem * ones(size(R));
    RGBT_record = [R, G, B, Tem_v];   % 合并成矩阵
    % 每一列分别是R, G, B, T, 图像坐标的row and column
    
    % 写入txt
    % fid = fopen('RGB_T_record.txt','w'); %写的方式打开文件（若不存在，建立文件）
    % fprintf(fid, RGBT_xy_record);  % %d 表示以整数形式写入数据
    % fclose(fid);  %关闭文件
    
    % 写入csv文件
    writematrix(RGBT_record, res_filename, 'WriteMode', 'append');
end

disp('--------------------get RGB program end (use data)--------------------')