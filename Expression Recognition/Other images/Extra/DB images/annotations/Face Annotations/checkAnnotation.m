function checkAnnotation(filename)

% Check Face Annotations Script
%
% Wilma Bainbridge, Michael Mack, Antonio Torralba, Aude Oliva
%
% A quick script to visualize the AAM points on an image
%
% Note: the .jpg file and the _landmarks.txt of the same label must be in
% the same folder for this to work.
%
% Usage: checkAnnotation(filename);
%    Ex: checkAnnotation('img.jpg');


set(0,'units','pixels');
screen= get(0,'screensize');

x = load([filename(1:(size(filename,2)-4)) '_landmarks.txt']);
img = double(imread(filename))/256;

figure
image(img)
axis('equal')
axis('tight')
set(gcf,'position',[10 40 screen(3)-30 screen(4)-120])
title(filename)

init=x;
hold on
h1= plot([init(9:24,1); init(9,1)],[init(9:24,2); init(9,2)],'ro-'); % face shape
h2= plot([init(46:53,1); init(46,1)],[init(46:53,2); init(46,2)],'go-'); % left eye
h3= plot([init(54:61,1); init(54,1)],[init(54:61,2); init(54,2)],'bo-'); % right eye
h4= plot([init(62:70,1); init(62,1)],[init(62:70,2); init(62,2)],'go-'); % upper lip
h5= plot([init(71:77,1); init(71,1)],[init(71:77,2); init(71,2)],'bo-'); % bottom lip
h6= plot([init(1:8,1); init(1,1)],[init(1:8,2); init(1,2)],'bo-'); % left eyebrow
h7= plot([init(25:32,1); init(25,1)],[init(25:32,2); init(25,2)],'go-'); % right eyebrow
h8= plot([init(33:45,1); init(33,1)],[init(33:45,2); init(33,2)],'ro-'); % nose
end
