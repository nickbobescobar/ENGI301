function plotter(filename)
    figure()
    data = load(filename);
    t = data(1,:);
    y = data(2,:);
    z = y;
    
    avgval = mean(z);
    z((z-avgval)>100) = avgval;
    
    plot(t,y,t,z)
    ylim([0 4096])
end