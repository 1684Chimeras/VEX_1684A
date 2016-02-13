import QtQuick 2.0
import QtQuick.Controls 1.4
Item {
    property bool clickable;
    property string tag;

    Rectangle{
        width: 705/6
        height: 444/5
        color: "#0000FF";
    }
    Label{
        text: tag;
    }
}

