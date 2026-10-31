% Grouped bar plot of the mean of the medians of the three samples, per
% position and hydrogel concentration (mean +/- SD).
% The values are the results of medians_per_position.m.

clear
clc
close all

%% Data: mean of the medians of the 3 samples (um) and SD, per position
positions = 1:3;
m12  = [1.00 0.88 1.13];   sd12 = [0.53 0.21 0.14];   % PEG-W 1.2%
m15  = [1.11 1.08 0.95];   sd15 = [0.53 0.56 0.55];   % PEG-W 1.5%

%% Colors
col12 = [0.11 0.25 0.45];   % dark blue
col15 = [0.80 0.35 0.10];   % orange

%% Figure (size in cm, to match text width)
fig = figure('Color','w', 'Units','centimeters', 'Position',[2 2 12 8.5]);
ax = axes(fig);
hold(ax, 'on')

% grouped bars
b = bar(ax, positions, [m12' m15'], 0.75, 'grouped', 'EdgeColor','none');
b(1).FaceColor = col12;
b(2).FaceColor = col15;

% error bars at the centre of each bar
x12 = b(1).XEndPoints;
x15 = b(2).XEndPoints;
errorbar(ax, x12, m12, sd12, 'k', 'LineStyle','none', 'LineWidth',1, 'CapSize',6);
errorbar(ax, x15, m15, sd15, 'k', 'LineStyle','none', 'LineWidth',1, 'CapSize',6);

% axes
xlim(ax, [0.4 3.6])
ylim(ax, [0 2])
xticks(ax, positions)
xlabel(ax, 'Position')
ylabel(ax, 'Median displacement towards the magnet (µm)', 'Interpreter', 'none')
set(ax, 'FontName','Arial', 'FontSize',10, 'LineWidth',1, ...
    'TickDir','out', 'Box','off')

legend(ax, b, {'PEG-W 1.2%', 'PEG-W 1.5%'}, 'Location','northeast', ...
    'Box','off', 'FontName','Arial', 'FontSize',9)

%% Export
exportgraphics(fig, 'validation_positions.png', 'Resolution', 300)
exportgraphics(fig, 'validation_positions.pdf', 'ContentType','vector')
