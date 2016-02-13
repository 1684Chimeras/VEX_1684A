import QtQuick 2.3
import QtQuick.Controls 1.2

Item {
    width: 1366;
    height: 566;
    //left side: drive controls
    //left side b = intake controls
    //right side b = shooter controls
    //right side  = arm controls

    Image{
        id: background
        source: "controls_background.png";
    }


    Item {
        id: driverControls
        width: 225
        height: 500
        x: 50
        y: 566/2 - 250
        Item {
            id: dcHeader

            width: 225
            height: 56

            Rectangle{
                id: dcHeaderBackground
                width: 225
                height: 56
                color: "#aaaaff"
            }

            Label{
                id: dcHeaderText
                text: "Driving"
                font.pixelSize: 36
                y: 5
            }
        }
        Item {
            id: dcContent
            y: 56
            width: 225
            height: 500 - 56
            Rectangle{
                id: dcContentBackground
                width: 225
                height: 500 - 56
                color: "#ffffff"
            }

            Label{
                id: dcContentText
                text: "content!!!"
            }
        }
    }

    Item {
        id: shooting
        width: 225
        height: 500
        x: 50 + 225 + 10
        y: 566/2 - 250
        Item {
            id: shHeader

            width: 225
            height: 56

            Rectangle{
                id: shHeaderBackground
                width: 225
                height: 56
                color: "#aaaaff"
            }

            Label{
                id: shHeaderText
                text: "Shooting"
                font.pixelSize: 36
                y: 5
            }
        }
        Item {
            id: shContent
            y: 56
            width: 225
            height: 500 - 56
            Rectangle{
                id: inContentBackground
                width: 225
                height: 500 - 56
                color: "#ffffff"
            }

            Label{
                id: shContentText
                text: "content!!!"
            }
        }
    }

    Item {
        id: arm
        width: 225
        height: 500
        x: 50 + 225 + 225 + 20
        y: 566/2 - 250
        Item {

            width: 225
            height: 56

            Rectangle{
                width: 225
                height: 56
                color: "#aaaaff"
            }

            Label{
                text: "Arm"
                font.pixelSize: 36
                y: 5
            }
        }
        Item {
            y: 56
            width: 225
            height: 500 - 56
            Rectangle{
                width: 225
                height: 500 - 56
                color: "#ffffff"
            }

            Label{
                text: "content!!!"
            }
        }
    }


    Label{
        text: "meow meowef awfD";
        anchors.centerIn: parent
        font.bold: true;
        font.pixelSize: 96;
        color: "steelblue"
    }
}

