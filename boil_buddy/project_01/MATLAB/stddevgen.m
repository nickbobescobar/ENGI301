function stddevgen(filename)
    data = load(filename);
    t = data(1,:);
    y = data(2,:);
    avgval = mean(y);
    y((y-avgval)>100) = avgval;
    
    devs = zeros(size(t));
    min_index = find(t>3, 1);
    for i = min_index:length(t)
        curr_time = t(i);
        from_index = find(t > (curr_time - 3),1);
        sample = y(from_index:i);
        resids = (sample - avgval).^2;
        devs(i-min_index+1) = sqrt(sum(resids)/(length(resids) - 1));
    end
    writematrix(devs,'devs.csv')
end