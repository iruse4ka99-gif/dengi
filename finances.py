import 'package:flutter/material.dart';

// Главный экран приложения
class FinanceDashboard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildHeader(),
              SizedBox(height: 30),
              _buildMainBalance(),
              SizedBox(height: 40),
              _buildEnvelopeGrid(),
              _buildQuickActionBtn(),
            ],
          ),
        ),
      ),
    );
  }

  // Заголовок с датой
  Widget _buildHeader() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text("МАРТ 2026", style: TextStyle(color: Colors.grey, letterSpacing: 2, fontSize: 12)),
        Icon(Icons.settings_outlined, color: Colors.white, size: 20),
      ],
    );
  }

  // Общий остаток (Центральный элемент)
  Widget _buildMainBalance() {
    return Center(
      child: Container(
        width: 180,
        height: 180,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          border: Border.all(color: Colors.greenAccent.withOpacity(0.2), width: 2),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("7,710 ₪", style: TextStyle(fontSize: 32, fontWeight: FontWeight.w200, color: Colors.white)),
            Text("ОСТАТОК", style: TextStyle(color: Colors.greenAccent, fontSize: 10, letterSpacing: 1)),
          ],
        ),
      ),
    );
  }

  // Сетка конвертов (Компонентный подход)
  Widget _buildEnvelopeGrid() {
    return Expanded(
      child: GridView.count(
        crossAxisCount: 2,
        crossAxisSpacing: 15,
        mainAxisSpacing: 15,
        children: [
          EnvelopeCard(title: "ЕДА", balance: 4000, limit: 4000, color: Colors.greenAccent),
          EnvelopeCard(title: "МАШИНА", balance: 500, limit: 1000, color: Colors.orangeAccent),
          EnvelopeCard(title: "АРИНА", balance: 100, limit: 100, color: Colors.blueAccent),
          EnvelopeCard(title: "НАТАН", balance: 100, limit: 100, color: Colors.purpleAccent),
        ],
      ),
    );
  }

  // Плавающая кнопка ввода (Главный CTA)
  Widget _buildQuickActionBtn() {
    return Center(
      child: Container(
        margin: EdgeInsets.only(bottom: 20),
        padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.05),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Colors.white.withOpacity(0.1)),
        ),
        child: Text("ВНЕСТИ ТРАТУ", style: TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.w500)),
      ),
    );
  }
}

// Виджет отдельного конверта
class EnvelopeCard extends StatelessWidget {
  final String title;
  final double balance;
  final double limit;
  final Color color;

  const EnvelopeCard({required this.title, required this.balance, required this.limit, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.03),
        borderRadius: BorderRadius.circular(24),
        border: Border(top: BorderSide(color: color, width: 2)),
      ),
      padding: EdgeInsets.all(20),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(title, style: TextStyle(color: Colors.grey, fontSize: 10, letterSpacing: 1)),
          SizedBox(height: 10),
          Text("${balance.toInt()} ₪", style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.w400)),
          SizedBox(height: 5),
          Text("${((balance/limit)*100).toInt()}%", style: TextStyle(color: color, fontSize: 10, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
