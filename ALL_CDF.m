d1 = dlmread('LongHop.txt',' ');
d1(:,length(d1)) = []
%linestyle = ['--','-'];
%color = ['r','b'];
%legendpos = 'Best';
%marker = ['s','o'];
lw = 4.0;
ms = 10;
fs = 16;

[h1, stat1] = cdfplot(d1);
set(h1, 'LineStyle','-','color','r','LineWidth',lw, 'Marker','o','MarkerSize',1);
%set(h1, 'LineStyle','-','color','r','LineWidth',lw);

title('Long Hop');
xlabel('Average Completion Time','FontSize', fs, 'FontName', 'Arial');
ylabel('');
%legend(legendkey,'Location', 'SouthEast');
set(gcf,'position',[100 100 636 400]);
set(gca, 'FontSize', fs, 'FontName', 'Arial','YGrid','on');

set(gcf,'PaperPositionMode','auto');
%print('-r0','-depsc', strcat(filename, '.eps'));

clear;