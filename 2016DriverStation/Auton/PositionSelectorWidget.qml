import QtQuick 2.0
import QtQuick.Controls 1.4

Item {
    width: 705
    height: 444

    Label {
        text: "HI"
    }

    Row {
        PositionSelectorButton {
            tag: "leftmost"
            clickable: true;
        }
        PositionSelectorButton {
            tag: "left"
            clickable: true;
        }
        PositionSelectorButton {
            tag: "center"
            clickable: true;
        }
        PositionSelectorButton {
            tag: "right"
            clickable: true;
        }
        PositionSelectorButton {
            tag: "rightmost"
            clickable: true;
        }
    }

    Rectangle {
        width: 705/6
        height: 444
        color: "#0000FF"
    }
}

