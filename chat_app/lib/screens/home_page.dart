import 'package:flutter/material.dart';
import 'package:chat_app/screens/chat_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          elevation: 0,
          automaticallyImplyLeading: false,
          backgroundColor: Theme.of(context).scaffoldBackgroundColor,
          flexibleSpace: SafeArea(
              child: Padding(
                  padding: const EdgeInsets.only(left: 16, right: 16, top: 10),
                  child: Stack(
                    children: [
                      const Align(
                          alignment: Alignment.topLeft,
                          child: CircleAvatar(
                            radius: 16,
                            backgroundImage:
                                NetworkImage("https://i.imgur.com/BoN9kdC.png"),
                          )),
                      const Align(
                          alignment: Alignment.center,
                          child: Expanded(
                              child: Center(
                                  child: Text(
                            "Messages",
                            style: TextStyle(
                                fontSize: 24, fontWeight: FontWeight.bold),
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
                  )))),
      body: const ChatPage(),
      bottomNavigationBar: BottomNavigationBar(
          selectedItemColor: Colors.blue,
          unselectedItemColor: Colors.grey.shade600,
          selectedLabelStyle: const TextStyle(fontWeight: FontWeight.w600),
          unselectedLabelStyle: const TextStyle(fontWeight: FontWeight.w600),
          type: BottomNavigationBarType.fixed,
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.chat_bubble_rounded),
              label: "Chats",
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.people_alt_rounded),
              label: "People",
            ),
          ]),
    );
  }
}
