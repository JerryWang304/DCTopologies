d1 = dlmread('DCell.txt',' ');
d2 = dlmread('F10.txt',' ');
d3 = dlmread('FatTree.txt',' ');
d4 = dlmread('FlattenedButterfly.txt',' ');
d5 = dlmread('HyperX.txt',' ');
d6 = dlmread('SWRing.txt',' ');
d7 = dlmread('SW2D.txt',' ');
d8 = dlmread('SW3D.txt',' ');
d9 = dlmread('LongHop.txt',' ');
d1(:,length(d1))=[]
d2(:,length(d2))=[]
d3(:,length(d3))=[]
d4(:,length(d4))=[]
d5(:,length(d5))=[]
d6(:,length(d6))=[]
d7(:,length(d7))=[]
d8(:,length(d8))=[]

d9(:,length(d9))=[]

lw = 4.0;
ms = 10;
fs = 16;

legendkey = {'DCell','F10','FatTree','FlattenedButterfly','HyperX','SWRing','SW2D','SW3D','Long Hop'};
figure;

[h1, stat1] = cdfplot(d1);

set(h1, 'LineStyle','-','color','r','LineWidth',lw);
hold on;
title('Compare Average Completion Time ');
[h2,stat2] = cdfplot(d2);
set(h2,'LineStyle','-','color','g','LineWidth',lw);
hold on;

[h3, stat3] = cdfplot(d3)
set(h3,'LineStyle','-','color','b','LineWidth',lw);
hold on;

[h4, stat4] = cdfplot(d4)
set(h4,'LineStyle','-','color','c','LineWidth',lw);
hold on;

[h5, stat5] = cdfplot(d5)
set(h5,'LineStyle','-','color','m','LineWidth',lw);
hold on;


[h6, stat6] = cdfplot(d6)
set(h6,'LineStyle','-','color','y','LineWidth',lw);
hold on;

[h7, stat7] = cdfplot(d7)
set(h7,'LineStyle','-','color','k','LineWidth',lw);
hold on;

[h8, stat8] = cdfplot(d8)
set(h3,'LineStyle','-','color',[0.5,0.5,0.5],'LineWidth',lw);
hold on;

[h9, stat9] = cdfplot(d9)
set(h9,'LineStyle','-','color',[1,0.9,0.8],'LineWidth',lw);
hold off;

xlabel('Average Completion Time','FontSize', fs, 'FontName', 'Arial');
ylabel('');
legend(legendkey,'Location','SouthEast');
set(gcf,'position',[100 100 636 400]);
set(gca, 'FontSize', fs, 'FontName', 'Arial','YGrid','on');

set(gcf,'PaperPositionMode','auto');
%print('-r0','-depsc', strcat(filename, '.eps'));

clear;