clear
clc
close all
disp('--------------------program begin--------------------')
%% 参数选择
% Tem_range = 15:16; % 调试程序
Tem_range = 15:39;
% num = 1:length(Tem_range)'; % 输出时的表格编号

sz = 9;     % 滤波窗的大小
row = 604;
col = 951;
%% 申请空间
% 记录每个温度的RGB的向量，每一行代表一个温度
R = zeros(size(Tem_range))'; % 列向量，后面要合并成矩阵，填到表格上   
G = R;
B = R;
% 记录选取点的坐标值
col_v = R;
row_v = R;
% 循环，对每一个温度提取一个RGB值
for Tem = Tem_range
    %% 图像读取与滤波
    filename = ['.\pic\', num2str(Tem), '.jpg'];
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
    
    %% 提取RGB值
    % 读取鼠标点的坐标值，鼠标交互
    disp(['温度: ', num2str(Tem)])
%     [x,y] = ginput(1);
%     col = round(x);
%     row = round(y);
%     disp(['coly坐标值: (', num2str(col), ', ', num2str(row), ')'])
    
    % 记录到RGB向量中
    R(Tem-14) = I(row, col, 1);
    G(Tem-14) = I(row, col, 2);
    B(Tem-14) = I(row, col, 3);
    
    % 记录coly坐标值到向量中，i.e.记录选取点
    col_v(Tem-14) = col;
    row_v(Tem-14) = row;

    disp(['RGB值：[', num2str(R(Tem-14)), ', ' num2str(G(Tem-14)), ...
        ', ' num2str(B(Tem-14)) ']'])
    disp('------------------------------')

end % end for

%% 合并矩阵，写入到表格中
RGBT_rc_record = [R, G, B, Tem_range', row_v, col_v];   % 合并成矩阵
% 每一列分别是R, G, B, T, 图像坐标的row and column

% 写入txt
% fid = fopen('RGB_T_record.txt','w'); %写的方式打开文件（若不存在，建立文件）
% fprintf(fid, RGBT_xy_record);  % %d 表示以整数形式写入数据
% fclose(fid);  %关闭文件

% 写入csv文件
csvwrite('RGBT_rc_at1point.csv', RGBT_rc_record);
disp('--------------------program end--------------------')