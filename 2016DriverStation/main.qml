import QtQuick 2.3
import QtQuick.Controls 1.2

import "main.js" as Main

//LEFT SIDE MENU:
//Top : DS
//Code Setup
//Controller Setup
//Code Editor
//Auton Editor
//RIO Setup (+ CAN setup)
//Settings

//idea for a window - PDP window - shows current draw of all channels
ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("DemoWidget")
    id: window

    function startupFunction() {
        setHeight(566);
        setWidth(1366);
        setX(0);
        setY(0);
        Main.setWindow(window, content);
    }

    Component.onCompleted: startupFunction();


    Rectangle {
        id: background;

        color: "#000000";

        width: 9999;
        height: 9999;
    }


    Item {
        id: content
        width: 1366
        height: 566

        Label {
            text: "NOT CONNECTED";
            anchors.centerIn: parent
            font.bold: true;
            font.pixelSize: 96;
        }

    }

    ControlMenuWidget {
        id: sideThing;
        x: 0;
    }

    EditingMenuHostWidget {
        id: topThing;
        x: 0;
        y: 0;
    }

}

