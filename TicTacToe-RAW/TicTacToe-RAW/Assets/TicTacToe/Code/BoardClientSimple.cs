using UnityEngine;
using System.Collections;
using System;
using System.IO;
using System.Threading;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
public class BoardClientSimple : MonoBehaviour {
    Board m_Board = new Board();
    
    Board.ePlayer e_MyPlayer = Board.ePlayer.eNone;
    public Board Board { get { return m_Board; } }

    Socket m_Socket = null;
    Thread m_ClientThread;

    bool b_CanPlay = true;

    Socket TryConnect()
    {
        Socket s = null;
        IPHostEntry hostEntry = null;

        // Get host related information.
        hostEntry = Dns.GetHostEntry("localhost");
        int port = 50000;
        // Loop through the AddressList to obtain the supported AddressFamily. This is to avoid
        // an exception that occurs when the host IP Address is not compatible with the address family
        // (typical in the IPv6 case).
        foreach(IPAddress address in hostEntry.AddressList)
        {
            IPEndPoint ipe = new IPEndPoint(address, port);
            Socket tempSocket = 
                new Socket(ipe.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

            try
            {
                tempSocket.Connect(ipe);
            }
            catch
            {
                Debug.Log(String.Format("No Server found at {0}:{1}", address, port));
            }

            if(tempSocket.Connected)
            {
                s = tempSocket;
                break;
            }
            else
            {
                continue;
            }
        }
        return s;
    }

    int GetInt()
    {
        Debug.Log("SALUUUT");
        byte[] buffer = new byte[1];
        Debug.Log("blabla : " + m_Socket.Receive(buffer,SocketFlags.None));
        string result = System.Text.Encoding.UTF8.GetString(buffer);
        Debug.Log(result);
        return int.Parse(result);
    }

    void InitServer()
    {
        while((m_Socket = TryConnect()) == null)
        {
            Debug.Log("Waiting for Server");
        }
        Debug.Log("Connected to Server");
        
            e_MyPlayer = (Board.ePlayer)GetInt();
            Debug.Log("YOYOYOO " + e_MyPlayer);
            m_Board.Init((Board.ePlayer)GetInt());
            Debug.Log("SALUUUT" + m_Board.GetCurrentTurnPlayer());
            while(Board.GetWinner() == Board.ePlayer.eNone)
            {
            Board.PlayerMove(GetInt());
            b_CanPlay = true;
        }
    }

    void SafeTerminate()
    {
        m_Socket.Close();
        Debug.Log("Killing thread");
        m_ClientThread.Abort();
    }
    // Use this for initialization
    void Start () 
    {
        Debug.Log("New Thread");
        ThreadStart startClient = new ThreadStart(InitServer);
        m_ClientThread = new Thread(startClient);
        m_ClientThread.Start();
    }
        //on start you could connect to the server immediately

    void OnApplicationQuit()
    {
        SafeTerminate();
    }
	// Update is called once per frame
	void Update () {

    }

    public void RequestMove(int istate)
    {
        Board.ePlayer e_Current = m_Board.GetCurrentTurnPlayer();
        if(b_CanPlay && e_Current != Board.ePlayer.eNone && e_Current == e_MyPlayer)
        {
            b_CanPlay = false;
            m_Socket.Send(System.Text.Encoding.UTF8.GetBytes(istate.ToString()));
        }
    }
}
