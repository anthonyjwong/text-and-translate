import 'package:flutter/material.dart';
import 'package:chat_app/models/chat_message_model.dart';
import 'package:colorful_safe_area/colorful_safe_area.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatDetailPage extends StatefulWidget {
  const ChatDetailPage({Key? key}) : super(key: key);

  @override
  State<ChatDetailPage> createState() => _ChatDetailPageState();
}

class _ChatDetailPageState extends State<ChatDetailPage> {
  List<ChatMessage> messages = [];

  void _getMessages() async {
    final response = await http.get(Uri.parse("http://localhost:3000/hello"));
    setState(() {
      messages = jsonDecode(response.body)["messages"]
          .map<ChatMessage>((data) => ChatMessage.fromJson(data))
          .toList();
    });
  }

  @override
  void initState() {
    super.initState();
    _getMessages();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        automaticallyImplyLeading: false,
        backgroundColor: Colors.white,
        flexibleSpace: SafeArea(
          child: Container(
              padding: const EdgeInsets.only(right: 16),
              child: Row(children: [
                IconButton(
                    onPressed: () {
                      Navigator.pop(context);
                    },
                    icon:
                        const Icon(Icons.arrow_back_ios, color: Colors.black)),
                const SizedBox(width: 2),
                // const CircleAvatar(
                //   backgroundImage: NetworkImage(
                //       "https://randomuser.me/api/portraits/men/5.jpg"),
                // ),
                const SizedBox(width: 12),
                Expanded(
                    child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                      const Text("Kriss Benwat",
                          style: TextStyle(
                              fontSize: 16, fontWeight: FontWeight.w600)),
                      const SizedBox(height: 6),
                      Text("Online",
                          style: TextStyle(
                              color: Colors.grey.shade600, fontSize: 13))
                    ])),
                const Icon(Icons.settings, color: Colors.black54)
              ])),
        ),
      ),
      body: Stack(children: [
        ListView.builder(
          itemCount: messages.length,
          shrinkWrap: true,
          padding: const EdgeInsets.only(top: 10, bottom: 100),
          physics: const BouncingScrollPhysics(),
          itemBuilder: (context, index) {
            return Container(
              padding: EdgeInsets.only(
                  left: 16,
                  right: 16,
                  top: (index > 0
                      ? (messages[index - 1].messageType ==
                              messages[index].messageType
                          ? 2
                          : 7)
                      : 2)),
              child: Align(
                alignment: (messages[index].messageType == "receiver"
                    ? Alignment.topLeft
                    : Alignment.topRight),
                child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      color: (messages[index].messageType == "receiver"
                          ? Colors.grey.shade200
                          : Colors.blue),
                    ),
                    padding: const EdgeInsets.all(12),
                    child: Text(
                      messages[index].messageContent,
                      style: TextStyle(
                          fontSize: 15,
                          color: (messages[index].messageType == "receiver"
                              ? Colors.black
                              : Colors.white)),
                    )),
              ),
            );
          },
        ),
        ColorfulSafeArea(
            color: Colors.white,
            child: Align(
                alignment: Alignment.bottomLeft,
                child: Container(
                    padding:
                        const EdgeInsets.only(left: 10, bottom: 10, top: 10),
                    height: 60,
                    width: double.infinity,
                    color: Colors.white,
                    child: Row(
                      children: [
                        // GestureDetector(
                        //     onTap: () {},
                        //     child: Container(
                        //         height: 30,
                        //         width: 30,
                        //         decoration: BoxDecoration(
                        //             color: Colors.Blue,
                        //             borderRadius: BorderRadius.circular(30)),
                        //         child: const Icon(Icons.add,
                        //             color: Colors.white, size: 20))),
                        const SizedBox(width: 15),
                        Expanded(
                          child: TextField(
                              decoration: InputDecoration(
                                  hintText: "Write message...",
                                  hintStyle:
                                      const TextStyle(color: Colors.black54),
                                  border: InputBorder.none,
                                  filled: true,
                                  fillColor: Colors.grey.shade100,
                                  contentPadding:
                                      const EdgeInsets.only(left: 17),
                                  focusedBorder: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(20),
                                      borderSide: BorderSide.none),
                                  enabledBorder: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(20),
                                      borderSide: BorderSide.none))),
                        ),
                        const SizedBox(width: 15),
                        FloatingActionButton(
                            onPressed: () {},
                            child: const Icon(Icons.send,
                                color: Colors.blue, size: 18),
                            backgroundColor: Colors.white,
                            elevation: 0)
                      ],
                    )))),
      ]),
    );
  }
}
