class ChatMessage {
  ChatMessage({required this.messageContent, required this.messageType});

  String messageContent;
  String messageType;

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      messageContent: json['messageContent'],
      messageType: json['messageType'],
    );
  }
}
