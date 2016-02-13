import QtQuick 2.0
import "main.js" as SceneChanger

Item {
    id: menuWidget;
    property bool shown: false;


    MouseArea{
        x: 0;
        y: 0;
        id: mouseArea;

        width: 2;
        height: 9990;

        hoverEnabled: true;
        onPositionChanged: {
            if(menuWidget.shown){
                if(mouse.x > 300){
                    menuWidget.shown = false;
                }
            }else{
                //if(mouse.x <= 1){
                    menuWidget.shown = true;
                //}
            }
            mouse.accepted = false;
        }

        onExited: {
           // menuWidget.shown = false;
        }

        states: State {
            name: "expanded";
            when: menuWidget.shown;
            PropertyChanges {
                target: mouseArea;
                width: 9999;
            }
        }
    }

    Item{
        id: movableContents;

        x: -300;

        width: 152;
        height: 9990;

        Rectangle{
            id: background;
            x: 0;
            y: 0;

            color: "#ff0000";
            height: 3000;
            width: movableContents.width;

            opacity: 0.4;
        }

        MenuWidgetOption{
            srcImage: "drivestation.png";
            onHit: {
                console.log("HI!!!");
                SceneChanger.to("DriverStationScene");
            }
            x: 0;
            y: 0;
        }

        MenuWidgetOption{
            srcImage: "auto.png";
            onHit: {
                console.log("HI");
                SceneChanger.to("AutonConfigScene");
            }

            x: 0;
            y: 205;
        }
        MenuWidgetOption{
            srcImage: "config.png";
            onHit: {
                console.log("HI");
                SceneChanger.to("ControllerSetupScene");
            }

            x: 0;
            y: 410;
        }
    }


    states: State{
        name: "shown";
        when: menuWidget.shown

        PropertyChanges {
            target: movableContents;
            x: 0;
        }
    }


    transitions: Transition{
        NumberAnimation {
            property: "x";
            duration: 200;
            easing.type: Easing.InOutQuad
        }
    }
}

