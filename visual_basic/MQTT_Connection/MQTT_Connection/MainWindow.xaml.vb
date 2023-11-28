Imports System
Imports System.IO
Imports System.Net
Imports System.Windows
Imports System.Threading
Imports System.Diagnostics.Eventing.Reader

' --- MQTT Imports ---
Imports uPLibrary.Networking.M2Mqtt
Imports uPLibrary.Networking.M2Mqtt.Messages
Imports uPLibrary.Networking.M2Mqtt.Exceptions

' --- JSON Imports
Imports Newtonsoft.Json
Imports Newtonsoft.Json.Linq


Class MainWindow
    Inherits Window
    Private client As MqttClient
    Private MQTT_CLIENT_ID As String = ""
    Private MQTT_USERNAME As String = ""
    Private MQTT_PASSWORD As String = ""
    Private MQTT_SERVER_URL As String = ""
    Private MQTT_SERVER_PORT As Integer = 0
    Private MQTT_TOPIC_TO_SEND As String = ""
    Private MQTT_TOPIC_TO_RECIEVE As String = ""

    Private Sub MainWindow_Loaded(sender As Object, e As RoutedEventArgs)

        'Get project main parent path
        Dim path As String = Directory.GetParent(Directory.GetCurrentDirectory()).Parent.FullName
        Console.WriteLine(path)





    End Sub
    Private Sub Button_Click(sender As Object, e As RoutedEventArgs)

    End Sub
End Class
