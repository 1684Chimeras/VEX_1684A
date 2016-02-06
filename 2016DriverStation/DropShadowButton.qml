import QtQuick 2.4
import QtGraphicalEffects 1.0

Item {
    property string image;
    property function onHit;

    id: button;

    width: 150;
    height: 150;

    Image{
        id: src
        source: image;
        anchors.fill: button;
    }

    MouseArea{
        id: hoverArea;
        width: 150;
        height: 150;
        hoverEnabled: true;
        property bool hovered: false;
        property bool clicked: false;

        onPositionChanged: {
            mouse.accepted = false;
        }

        onEntered: {
            hovered = true;
        }
        onExited: {hovered = false; console.log("Exited!");}

        onPressed: {clicked = true; console.log("Clicked") onHit();
            }
        onReleased: {clicked = false; console.log("Released!")}
    }


    Text{
        text: "NO IMAGE";
    }

    DropShadow{
        id: dropShadow;
        anchors.fill: src;
        radius: 32.0;
        samples: 32;
        horizontalOffset: 3;
        verticalOffset: 3;
        color: "#b00000000";
        source: src;

        states: [ State{
            name: "hovered";
            when: hoverArea.hovered && !hoverArea.clicked

            PropertyChanges {
                target: dropShadow;
                radius: 32;
            }
        }, State{
            name: "clicked"
            when: hoverArea.clicked;

            PropertyChanges{
                target: dropShadow;
                radius: 4;
                color: "#00000000";
            }
        }]


        transitions: [Transition{
            NumberAnimation {
                property: "radius";
                duration: 100;
                easing.type: Easing.InOutQuad
            }
        }, Transition{
            NumberAnimation{
                property: "color";
                duration: 100;
                easing.type: Easing.InOutQuad
            }
        }]
    }
    InnerShadow {

        id: innerShadow;
        anchors.fill: src;
        radius: 16.0;
        samples: 32;
        horizontalOffset: 0;
        verticalOffset: 0;
        color: "#b00000000";
        source: src;

        states: [ State{
            name: "hovered";
            when: hoverArea.hovered && !hoverArea.clicked

            PropertyChanges {
                target: innerShadow;
                radius: 32;
            }
        }, State{
            name: "clicked"
            when: hoverArea.clicked;

            PropertyChanges{
                target: innerShadow;
                radius: 48;
                color: "#d0000000";
            }
        }]


        transitions: [Transition{
            NumberAnimation {
                property: "radius";
                duration: 100;
                easing.type: Easing.InOutQuad
            }
        }, Transition{
            NumberAnimation{
                property: "color";
                duration: 100;
                easing.type: Easing.InOutQuad
            }
        }]
    }

}

