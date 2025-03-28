% Script to convert sideways .mat matrices into CSV files with proper headers

% Define files: {input .mat, output .csv, column names}
fileList = {
    './mat_files/active_power.mat',  'simulink_p.csv',     {'time', 'p'};
    './mat_files/reactive_power.mat','simulink_q.csv',     {'time', 'q'};
    './mat_files/vabcpu.mat',          'simulink_vabc.csv',  {'time', 'v_a', 'v_b', 'v_c'};
    './mat_files/iabc.mat',          'simulink_iabc.csv',  {'time', 'i_a', 'i_b', 'i_c'};
};

for k = 1:size(fileList, 1)
    matFile  = fileList{k, 1};
    csvFile  = fileList{k, 2};
    colNames = fileList{k, 3};

    % Load and extract the raw matrix
    data = load(matFile);
    raw = struct2cell(data);
    mat = raw{1};  % Extract the actual matrix

    % Transpose to get rows as time series (N x variables)
    mat = mat';

    % Convert to table with correct column names
    T = array2table(mat, 'VariableNames', colNames);

    % Write to CSV
    writetable(T, csvFile);
    fprintf('Saved: %s (%d rows)\n', csvFile, height(T));
end

