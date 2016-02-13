import QtQuick 2.0

Item {
    property string image;
    signal click;

    width: 200
    height: 200
    Image{
        source: "Auton/"+image+".png";
    }
    MouseArea{
        width: 200
        height: 200;

        onReleased: click();
    }
}

