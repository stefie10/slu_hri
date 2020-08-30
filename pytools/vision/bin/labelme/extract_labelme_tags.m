%labelme tester

%D = load('lmdatabase.mat');
s = size(D.D)


file1 = fopen('labelme_objects.txt', 'w');
for i=1:s(2)
    %'**************************************************'
    
    try
        %D.D(i).annotation;

        objects = D.D(i).annotation.object;
        

        s2 = size(objects);


        %D.D(i).annotation
        fprintf(file1, '%s, ', D.D(i).annotation.filename);
        fprintf(file1, '%s, ', D.D(i).annotation.folder);
        fprintf(file1, '%s, ', D.D(i).annotation.scenedescription);

        for j=1:s2(2)
            fprintf(file1, '%s, ',objects(j).name);
        end
        fprintf(file1, '\n');
    catch
        'No object field'
    end
    
end