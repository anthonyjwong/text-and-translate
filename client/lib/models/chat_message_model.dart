class ChatMessage {
  static const String user = "fdd0de83-263e-4981-ab40-957091339396";
  ChatMessage(
      {required this.messageContent,
      required this.messageType,
      required this.sentAt});

  String messageContent;
  String messageType;
  String sentAt;

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
        messageContent: json['message_content'],
        messageType: json['sender'] == user // hard coded for prototype
            ? 'sender'
            : 'receiver',
        sentAt: json['sent_at']);
  }
}
