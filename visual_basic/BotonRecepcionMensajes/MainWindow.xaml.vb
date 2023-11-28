Imports uPLibrary.Networking.M2Mqtt
Imports uPLibrary.Networking.M2Mqtt.Messages
Imports System
Imports System.Windows
Imports System.Threading
Imports System.Net
Imports uPLibrary.Networking.M2Mqtt.Exceptions
Imports System.Diagnostics.Eventing.Reader
Imports Newtonsoft.Json
Imports System.IO
Partial Public Class MainWindow
    Inherits Window
    Private client As MqttClient
    Private topic As String = ""

    Private Sub MainWindow_Loaded(sender As Object, e As RoutedEventArgs)
        'Cargando variables con información temporal
        Dim MQTT_CLIENT_ID As String = "VBClienteRecepcion"
        Dim MQTT_USERNAME As String = ""
        Dim MQTT_PASSWORD As String = ""
        Dim MQTT_SERVER_URL As String = ""
        Dim MQTT_SERVER_PORT As Integer = 1
        'Cargando las variables de MQTT desde el archivo config.json
        Try
            Dim configFile As String = "config.json"
            Dim configJson As String = File.ReadAllText(configFile)
            'Dim config As Config = JsonConvert.DeserializeObject(Of Config)(configJson)

            Console.WriteLine("Archivo cargado correctamente")

        Catch ex As Exception
            Console.WriteLine("El archivo no se pudo cargar")
        End Try

        Console.WriteLine(vbCrLf & vbCrLf & vbCrLf & "Inicio..." & vbCrLf & vbCrLf & vbCrLf)



        client = New MqttClient("10.10.10.103", 1883, False, Nothing, Nothing, MqttSslProtocols.None)

        client.Connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)

        If client.IsConnected Then
            client.Subscribe(New String() {topic}, New Byte() {MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE})
            Console.WriteLine("Conectado al tema: " & topic)
        Else
            Console.WriteLine("No se pudo conectar al tema")
        End If
        AddHandler client.MqttMsgPublishReceived, AddressOf MessageReceived
    End Sub
    Private Sub Button_Click(sender As Object, e As RoutedEventArgs)
        Try
            ' Get the message from a TextBox or any other input control
            Dim messageToSend As String = "Hello, MQTT!"
            client.Publish(topic, System.Text.Encoding.UTF8.GetBytes(messageToSend), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, False)

            ' Check if the client is connected before publishing
            If client.IsConnected Then
                ' Publish the message to the specified topic
                Console.WriteLine("Mensaje enviado: " & messageToSend)
            Else
                Console.WriteLine("No se pudo enviar el mensaje. Cliente MQTT no está conectado.")
            End If
        Catch ex As Exception
            Console.WriteLine("Error al enviar el mensaje: " & ex.Message)
        End Try
    End Sub
    Private Sub MessageReceived(sender As Object, e As MqttMsgPublishEventArgs)
        Dim message As String = System.Text.Encoding.UTF8.GetString(e.Message)
        Console.WriteLine("Mensaje recibido: " & message)
    End Sub

    Private Sub MainWindow_Closing(sender As Object, e As ComponentModel.CancelEventArgs)
        If client.IsConnected Then
            client.Disconnect()
        End If
    End Sub

End Class
