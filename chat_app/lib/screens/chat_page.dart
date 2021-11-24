import 'package:flutter/material.dart';
import 'package:chat_app/models/chat_users_model.dart';

class ChatPage extends StatefulWidget {
  const ChatPage({Key? key}) : super(key: key);

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  List<ChatUsers> chatUsers = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                SafeArea(
                    child: Padding(
                        padding:
                            const EdgeInsets.only(left: 16, right: 16, top: 10),
                        child: Stack(
                          children: <Widget>[
                            Align(
                                alignment: Alignment.topLeft,
                                child: Container(
                                    width: 32,
                                    height: 32,
                                    decoration: const BoxDecoration(
                                        shape: BoxShape.circle,
                                        image: DecorationImage(
                                            fit: BoxFit.fill,
                                            image: NetworkImage(
                                                "https://i.imgur.com/BoN9kdC.png"))))),
                            const Align(
                                alignment: Alignment.center,
                                child: Expanded(
                                    child: Center(
                                        child: Text(
                                  "Chats",
                                  style: TextStyle(
                                      fontSize: 24,
                                      fontWeight: FontWeight.bold),
                                )))),
                            Align(
                                alignment: Alignment.topRight,
                                child: Container(
                                  padding: const EdgeInsets.only(
                                      left: 8, right: 8, top: 2, bottom: 2),
                                  height: 30,
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(30),
                                    color: Colors.blue[50],
                                  ),
                                  child: const Icon(
                                    Icons.create_rounded,
                                    color: Colors.blue,
                                    size: 20,
                                  ),
                                )),
                          ],
                        )))
              ])),
    );
  }
}
