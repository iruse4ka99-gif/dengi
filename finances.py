import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { Feather } from '@expo/vector-icons'; // Иконки

const BudgetApp = () => {
  return (
    <View style={styles.container}>
      {/* HEADER */}
      <View style={styles.header}>
        <Text style={styles.month}>МАРТ 2026</Text>
        <Text style={styles.balance}>4,520 ₪</Text>
        <Text style={styles.subtext}>Безопасно потратить</Text>
      </View>

      {/* КАТЕГОРИИ */}
      <ScrollView contentContainerStyle={styles.grid}>
        <CategoryCard name="Лео" amount="600" color="#30d158" />
        <CategoryCard name="Продукты" amount="1,200" color="#ff9f0a" />
        <CategoryCard name="Разное" amount="320" color="#ff3b30" />
      </ScrollView>

      {/* ГЛАВНАЯ КНОПКА + */}
      <TouchableOpacity style={styles.fab}>
        <Feather name="plus" size={32} color="white" />
      </TouchableOpacity>
    </View>
  );
};

// Компонент карточки для чистоты кода
const CategoryCard = ({ name, amount, color }) => (
  <View style={styles.card}>
    <Text style={styles.cardLabel}>{name.toUpperCase()}</Text>
    <Text style={styles.cardAmount}>{amount} ₪</Text>
    <View style={[styles.progress, { backgroundColor: color, width: '70%' }]} />
  </View>
);

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F2F2F7' },
  header: { padding: 40, alignItems: 'center', backgroundColor: '#FFF', borderBottomLeftRadius: 32, borderBottomRightRadius: 32 },
  month: { color: '#8E8E93', fontSize: 13, fontWeight: '600', letterSpacing: 1 },
  balance: { fontSize: 54, fontWeight: '300', color: '#1C1C1E', marginVertical: 8 },
  subtext: { color: '#30d158', fontWeight: '700', fontSize: 12 },
  grid: { padding: 20, flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' },
  card: { backgroundColor: '#FFF', width: '48%', borderRadius: 24, padding: 20, marginBottom: 15, shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 10 },
  cardLabel: { color: '#8E8E93', fontSize: 10, fontWeight: '700' },
  cardAmount: { fontSize: 24, color: '#1C1C1E', marginVertical: 5 },
  progress: { height: 4, borderRadius: 2 },
  fab: { position: 'absolute', bottom: 40, alignSelf: 'center', backgroundColor: '#30d158', width: 70, height: 70, borderRadius: 35, alignItems: 'center', justifyContent: 'center', shadowColor: '#30d158', shadowOpacity: 0.4, shadowRadius: 15 }
});

export default BudgetApp;
