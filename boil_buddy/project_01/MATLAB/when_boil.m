function when_boil(filename)
    check_time = 5;
    sample_duration = 15;
    
    data = load(filename);
    time = data(1,:);
    vals = data(2,:);
    
    sample_size = find(time >= sample_duration,1);
    
    histogram(vals(1:sample_size))
    title("Initial")
    figure()
    histogram(vals(end-sample_size:end))
    title("Final")
    
end