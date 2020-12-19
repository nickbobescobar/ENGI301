function liveplot
    close all
    
    display_time = 10;
    sensor = serialport("COM3",115200);
    
    t = 0;
    val = 0;
    
    
    tic
    while 1 == 1
        data_in = str2num(readline(sensor));
        new_t = data_in(1,:);
        new_val = data_in(2,:);
        t = [t new_t];
        val = [val new_val];

        plot(t,val)
        %semilogy(t,val)
        %xlim([t(end)-display_time,t(end)])
        xlim([0 t(end)])
        ylim([0,4096])
        drawnow();
        
        pause(0.25)
    end
end