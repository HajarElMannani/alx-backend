import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const app = express();
const products = [
    {itemId: 1, itemName: 'Suitcase 250',  price:  50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450',  price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650',  price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];
finction getItemById(id) {
  return listProducts.find(produc => produc.itemId === id);
}
const client = createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);
function reserveStockById(itemId, stock) {
  return setAsync(`item.${itemId}`, stock.toString());
}
async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return number(stock) || 0;
}
app.get('/list_products', (req, res) => {
  res.json(products);
});
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);
  if (!item) {
    return res.json({ status: 'Product not found' });
  }
  const reserved = await getCurrentReservedStockById(itemId);
  const currentQuantity = item.initialAvailableQuantity - reserved;
  res.json({ ...item, currentQuantity });
});
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);
  if (!item) {
    return res.json({ status: 'Product not found' });
  }
  const reserved = await getCurrentReservedStockById(itemId);
  if (reserved >= item.initialAvailableQuantity) {
    return res.json({ status: 'Not enough stock available', itemId });
  }
  await reserveStockById(itemId, reserved + 1);
  res.json({ status: 'Reservation confirmed', itemId});
});
app.listen(1245);
