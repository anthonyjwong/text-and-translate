import 'package:chat_app/screens/chat_detail_page.dart';
import 'package:flutter/material.dart';

class ConversationList extends StatefulWidget {
  const ConversationList(
      {Key? key,
      required this.name,
      required this.messageText,
      required this.imageURL,
      required this.time,
      required this.isMessageRead})
      : super(key: key);

  final String name;
  final String messageText;
  final String imageURL;
  final String time;
  final bool isMessageRead;

  @override
  State<ConversationList> createState() => _ConversationListState();
}

class _ConversationListState extends State<ConversationList> {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
        onTap: () {
          Navigator.push(context, MaterialPageRoute(builder: (context) {
            return const ChatDetailPage();
          }));
        },
        child: Container(
            padding:
                const EdgeInsets.only(left: 16, right: 16, top: 10, bottom: 10),
            child: Row(children: [
              Expanded(
                  child: Row(children: [
                CircleAvatar(
                  backgroundImage: NetworkImage(widget.imageURL),
                  maxRadius: 30,
                ),
                const SizedBox(
                  width: 16,
                ),
                Expanded(
                  child: Container(
                    color: Colors.transparent,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(widget.name, style: const TextStyle(fontSize: 16)),
                        const SizedBox(height: 6),
                        Text(widget.messageText,
                            style: TextStyle(
                                fontSize: 13,
                                color: Colors.grey.shade600,
                                fontWeight: widget.isMessageRead
                                    ? FontWeight.normal
                                    : FontWeight.bold))
                      ],
                    ),
                  ),
                )
              ])),
              Text(widget.time,
                  style: TextStyle(
                      fontSize: 12,
                      fontWeight: widget.isMessageRead
                          ? FontWeight.normal
                          : FontWeight.bold))
            ])));
  }
}
