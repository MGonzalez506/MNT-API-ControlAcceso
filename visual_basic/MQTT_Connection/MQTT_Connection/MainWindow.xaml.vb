﻿Imports System
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
    Private projectDirectory As String

    Private Sub MainWindow_Loaded(sender As Object, e As RoutedEventArgs)

        Try
            'Get project main parent path
            Dim path As String = Directory.GetParent(Directory.GetCurrentDirectory()).Parent.FullName

            Dim currentDirectory As String = Directory.GetCurrentDirectory()
            Dim parentDirectory As String = Directory.GetParent(currentDirectory).FullName
            Dim grandparentDirectory As String = Directory.GetParent(parentDirectory).FullName
            projectDirectory = Directory.GetParent(grandparentDirectory).FullName


            'Read .env and parse it as json
            Dim json As JObject = JObject.Parse(File.ReadAllText(projectDirectory + "\.env"))
            'Console.WriteLine(path)


            MQTT_CLIENT_ID = json.SelectToken("Cliente_ID").ToString()
            MQTT_USERNAME = json.SelectToken("Cliente_Username").ToString()
            MQTT_PASSWORD = json.SelectToken("Cliente_Password").ToString()
            MQTT_SERVER_URL = json.SelectToken("MQTT_SERVER_HOST").ToString()
            MQTT_SERVER_PORT = json.SelectToken("MQTT_SERVER_PORT")
            MQTT_TOPIC_TO_SEND = json.SelectToken("TEMA_PARA_ENVIO").ToString()
            MQTT_TOPIC_TO_RECIEVE = json.SelectToken("TEMA_PARA_RECEPCION").ToString()

            Console.WriteLine("Cliente_ID: " & MQTT_CLIENT_ID)
            Console.WriteLine("Cliente_Username: " & MQTT_USERNAME)
            Console.WriteLine("Cliente_Password: " & MQTT_PASSWORD)
            Console.WriteLine("MQTT_SERVER_HOST: " & MQTT_SERVER_URL)
            Console.WriteLine("MQTT_SERVER_PORT: " & MQTT_SERVER_PORT.ToString())
            Console.WriteLine("TEMA_PARA_ENVIO: " & MQTT_TOPIC_TO_SEND)
            Console.WriteLine("TEMA_PARA_RECEPCION: " & MQTT_TOPIC_TO_RECIEVE)


        Catch ex As Exception
            MessageBox.Show("Error al leer el archivo con las credenciales, saliendo del programa...")
            Application.Current.Shutdown()
        End Try

        client = New MqttClient(MQTT_SERVER_URL, MQTT_SERVER_PORT, False, Nothing, Nothing, MqttSslProtocols.None)

        Try
            client.Connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)
            Thread.Sleep(2000)

            If client.IsConnected Then
                client.Subscribe(New String() {MQTT_TOPIC_TO_RECIEVE}, New Byte() {MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE})
            Else
                MessageBox.Show("Error al conectarse al servidor MQTT, saliendo del programa...")
                Application.Current.Shutdown()
            End If
            AddHandler client.MqttMsgPublishReceived, AddressOf MessageReceived
        Catch ex As Exception
            MessageBox.Show("Error al conectarse al servidor MQTT, saliendo del programa...")
            Application.Current.Shutdown()
        End Try

    End Sub

    Private Sub MessageReceived(sender As Object, e As MqttMsgPublishEventArgs)
        Dim message As String = System.Text.Encoding.UTF8.GetString(e.Message)
        Console.WriteLine("Mensaje recibido: " & message)
    End Sub

    Private Sub MainWindow_Closing(sender As Object, e As ComponentModel.CancelEventArgs)
        If client.IsConnected Then
            client.Disconnect()
            Console.WriteLine("Desconectado de MQTT")
        End If
        Thread.Sleep(900)
    End Sub

    Private Sub btn_01_Click(sender As Object, e As RoutedEventArgs) Handles btn_01.Click

    End Sub

    Private Sub btn_02_Click(sender As Object, e As RoutedEventArgs) Handles btn_02.Click
        Try
            ' Lee el contenido del archivo JSON
            Dim jsonContent As String = File.ReadAllText(projectDirectory + "\agregar_usuario_sin_foto.json")

            ' Publica el contenido en el tema MQTT
            Dim messageBytes As Byte() = System.Text.Encoding.UTF8.GetBytes(jsonContent)
            client.Publish(MQTT_TOPIC_TO_SEND, messageBytes)

            Console.WriteLine("Archivo JSON enviado correctamente.")
        Catch ex As Exception
            MessageBox.Show("Error al enviar el archivo JSON al servidor MQTT: " & ex.Message)
        End Try
    End Sub

    Private Sub btn_03_Click(sender As Object, e As RoutedEventArgs) Handles btn_03.Click
        Try
            ' Lee el contenido del archivo JSON
            Dim jsonContent As String = File.ReadAllText(projectDirectory + "\actualizar_nivel_de_acceso.json")

            ' Publica el contenido en el tema MQTT
            Dim messageBytes As Byte() = System.Text.Encoding.UTF8.GetBytes(jsonContent)
            client.Publish(MQTT_TOPIC_TO_SEND, messageBytes)

            Console.WriteLine("Archivo JSON enviado correctamente.")
        Catch ex As Exception
            MessageBox.Show("Error al enviar el archivo JSON al servidor MQTT: " & ex.Message)
        End Try
    End Sub

    Private Sub btn_04_Click(sender As Object, e As RoutedEventArgs) Handles btn_04.Click
        Try
            ' Lee el contenido del archivo JSON
            Dim jsonContent As String = File.ReadAllText(projectDirectory + "\obtener_informacion_de_persona_por_id.json")

            ' Publica el contenido en el tema MQTT
            Dim messageBytes As Byte() = System.Text.Encoding.UTF8.GetBytes(jsonContent)
            client.Publish(MQTT_TOPIC_TO_SEND, messageBytes)

            Console.WriteLine("Archivo JSON enviado correctamente.")
        Catch ex As Exception
            MessageBox.Show("Error al enviar el archivo JSON al servidor MQTT: " & ex.Message)
        End Try
    End Sub

    Private Sub btn_05_Click(sender As Object, e As RoutedEventArgs) Handles btn_05.Click
        Try
            ' Lee el contenido del archivo JSON
            Dim jsonContent As String = File.ReadAllText(projectDirectory + "\editar_usuario.json")

            ' Publica el contenido en el tema MQTT
            Dim messageBytes As Byte() = System.Text.Encoding.UTF8.GetBytes(jsonContent)
            client.Publish(MQTT_TOPIC_TO_SEND, messageBytes)

            Console.WriteLine("Archivo JSON enviado correctamente.")
        Catch ex As Exception
            MessageBox.Show("Error al enviar el archivo JSON al servidor MQTT: " & ex.Message)
        End Try
    End Sub

    Private Sub btn_06_Click(sender As Object, e As RoutedEventArgs) Handles btn_06.Click
        Try
            ' Lee el contenido del archivo JSON
            Dim jsonContent As String = File.ReadAllText(projectDirectory + "\editar_rostro.json")

            ' Publica el contenido en el tema MQTT
            Dim messageBytes As Byte() = System.Text.Encoding.UTF8.GetBytes(jsonContent)
            client.Publish(MQTT_TOPIC_TO_SEND, messageBytes)

            Console.WriteLine("Archivo JSON enviado correctamente.")
        Catch ex As Exception
            MessageBox.Show("Error al enviar el archivo JSON al servidor MQTT: " & ex.Message)
        End Try
    End Sub

    Private Sub btn_07_Click(sender As Object, e As RoutedEventArgs) Handles btn_07.Click
        Try
            ' Lee el contenido del archivo JSON
            Dim jsonContent As String = File.ReadAllText(projectDirectory + "\eliminar_usuario.json")

            ' Publica el contenido en el tema MQTT
            Dim messageBytes As Byte() = System.Text.Encoding.UTF8.GetBytes(jsonContent)
            client.Publish(MQTT_TOPIC_TO_SEND, messageBytes)

            Console.WriteLine("Archivo JSON enviado correctamente.")
        Catch ex As Exception
            MessageBox.Show("Error al enviar el archivo JSON al servidor MQTT: " & ex.Message)
        End Try
    End Sub

    Private Sub btn_salir_Click(sender As Object, e As RoutedEventArgs) Handles btn_salir.Click
        client.Disconnect()
        Me.Close()
    End Sub
End Class
