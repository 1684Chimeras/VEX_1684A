#include <QApplication>
#include <QQmlApplicationEngine>

#include <vlc-qt/include/VLCQtCore/Common.h>

int main(int argc, char *argv[])
{

    QApplication app(argc, argv);
    //VlcCommon::setPluginPath(app.applicationDirPath() + "/plugins");

    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));

/*
 *
    QGuiApplication application(argc, argv);
    const QString mainQmlApp = QStringLiteral("qrc:///flickr.qml");
    QQuickView view;
    view.setSource(QUrl(mainQmlApp));
    view.setResizeMode(QQuickView::SizeRootObjectToView);
    // Qt.quit() called in embedded .qml by default only emits
    // quit() signal, so do this (optionally use Qt.exit()).
    QObject::connect(view.engine(), SIGNAL(quit()), qApp, SLOT(quit()));
    view.setGeometry(QRect(100, 100, 360, 640));
    view.show();
    return application.exec();
    */


    return app.exec();
}

