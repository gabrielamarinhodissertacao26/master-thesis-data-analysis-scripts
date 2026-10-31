% Percentage of displacement vectors per dominant displacement direction
% (+X, -X, +Y, -Y, +Z, -Z), obtained from the displacement field computed
% by TFMLAB (tp_01.mat).
%
% Input: tp_01.mat file(s) in the folder defined in dataFolder.
% Output: bar plot (displacement_direction.png / .pdf).

clear
clc
close all

%% Input (edit the path)
dataFolder = 'path/to/D_2_displacements/beads';
files = dir(fullfile(dataFolder, 'tp_01.mat'));

countDir = zeros(6,1);
for k = 1:numel(files)
    fprintf('Processing %s\n', files(k).name)
    S = load(fullfile(files(k).folder, files(k).name));
    X = S.dispField.X(:);
    Y = S.dispField.Y(:);
    Z = S.dispField.Z(:);

    % remove NaNs
    valid = ~(isnan(X) | isnan(Y) | isnan(Z));
    X = X(valid);
    Y = Y(valid);
    Z = Z(valid);

    % dominant direction (vectorized)
    A = [X Y Z];
    [~, idx] = max(abs(A), [], 2);
    signX = X >= 0;
    signY = Y >= 0;
    signZ = Z >= 0;
    dirIdx = zeros(size(idx));
    dirIdx(idx == 1 &  signX) = 1;
    dirIdx(idx == 1 & ~signX) = 2;
    dirIdx(idx == 2 &  signY) = 3;
    dirIdx(idx == 2 & ~signY) = 4;
    dirIdx(idx == 3 &  signZ) = 5;
    dirIdx(idx == 3 & ~signZ) = 6;
    countDir = countDir + accumarray(dirIdx, 1, [6 1]);
end

%% Conversion to percentage
totalDisp = sum(countDir);
pctDir = 100 * countDir / totalDisp;
fprintf('Total valid displacements: N = %d\n', totalDisp)

%% Figure (size in cm, to match text width)
labels = {'+X','-X','+Y','-Y','+Z','-Z'};
fig = figure('Color','w', 'Units','centimeters', 'Position',[2 2 12 8]);
b = bar(pctDir);

% single color for all bars
b.FaceColor = [0.10 0.25 0.45];
b.EdgeColor = 'none';
b.BarWidth = 0.7;

ax = gca;
set(ax, ...
    'FontName','Arial', ...
    'FontSize',10, ...
    'LineWidth',1, ...
    'TickDir','out', ...
    'Box','off')
xticks(1:6)
xticklabels(labels)
xlabel('Dominant displacement direction', 'FontWeight','normal')
ylabel('Displacement vectors (%)', 'FontWeight','normal')
grid off   % no title and no grid (values are written on the bars)

%% Bar labels
for i = 1:6
    text(i, pctDir(i) + 0.02*max(pctDir), sprintf('%.1f%%', pctDir(i)), ...
        'HorizontalAlignment','center', ...
        'VerticalAlignment','bottom', ...
        'FontName','Arial', ...
        'FontSize',9, ...
        'FontWeight','normal', ...
        'Color',[0.25 0.25 0.25]);
end

% top margin
ylim([0 max(pctDir)*1.15])

%% Export
exportgraphics(fig, 'displacement_direction.png', 'Resolution', 300)
exportgraphics(fig, 'displacement_direction.pdf', 'ContentType','vector')
