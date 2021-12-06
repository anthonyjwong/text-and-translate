class ChatMessage {
  static const user = "643cd96a-3034-46a4-b757-6a1161dcce26";
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
