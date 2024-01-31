% 读取水下彩色图像
originalImage = imread('D:\d_code\other\Project\water\5015.jpg');
output_path = 'D:\d_code\other\Project\water\result\result\局部直方图均衡化\5015.jpg';
% 暗通道先验去雾
Im=originalImage;
I=double(Im)/255; 
[m,n]=size(I,1,2);
w0=0.20;
wh=3;
%% dark_channel
I1=zeros(m,n);
for i=1:m
    for j=1:n
        I1(i,j)=min(I(i,j,:));
    end
end
Id = ordfilt2(I1,1,ones(wh,wh),'symmetric');
%%  A
dark_channel = Id;
A_temp = max(max(dark_channel))*0.999;
A=A_temp;
tr= 1 - w0 * Id/ A;
%% out 
t0=0.1;
t1 = max(t0,tr);
I_out=zeros(m,n,3);
for k=1:3
    for i=1:m
        for j=1:n
            I_out(i,j,k)=(I(i,j,k)-A)/t1(i,j)+A;
        end
    end
end




%白平衡

imgR = I_out(:,:,1);
imgG = I_out(:,:,2);
imgB = I_out(:,:,3);
RAve = mean2(imgR);
GAve = mean2(imgG);
BAve = mean2(imgB);
aveGray = (RAve+GAve + BAve) / 3;
%%第二步，计算三个通道的增益系数
RCoef = aveGray / RAve *0.4;
GCoef = aveGray / GAve;
BCoef = aveGray / BAve;
%%第三步，使用增益系数来调整原始图像
%disp(['RCorrection: ' num2str(RCorrection) ', GCorrection: ' num2str(GCorrection) ', BCorrection: ' num2str(BCorrection)]);
RCorrection = RCoef* imgR;%水下图片红色较少
GCorrection = GCoef * imgG;
BCorrection = BCoef * imgB;
imgDst=I_out;
imgDst(:,:,1) = RCorrection;
imgDst(:,:,2) = GCorrection;
imgDst(:,:,3) = BCorrection;

% 设定局部直方图均衡化的块大小
blockSize = 2;

% 分离RGB通道
redChannel = imgDst(:, :, 1);
greenChannel = imgDst(:, :, 2);
blueChannel = imgDst(:, :, 3);

% 应用局部直方图均衡化到每个通道
enhancedRedChannel = adapthisteq(redChannel, 'NumTiles', [blockSize, blockSize]);
enhancedGreenChannel = adapthisteq(greenChannel, 'NumTiles', [blockSize, blockSize]);
enhancedBlueChannel = adapthisteq(blueChannel, 'NumTiles', [blockSize, blockSize]);

% 合并增强后的通道
enhancedColorImage = cat(3, enhancedRedChannel, enhancedGreenChannel, enhancedBlueChannel);% 创建对比图
imwrite(enhancedColorImage,output_path);