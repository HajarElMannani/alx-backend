import express from 'express';
import kue from 'kue'
import { createClient } from 'redis';
import { promisify } from 'util';

const app = express();
const client = createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);
function reserveSeat(number) {
  return setAsync('available-seats', number.toString());
}
async function getCurrentAvailableSeats() {
  const value = await getAsync('available-seats');
  return Number(value);
}
reserveSeat(50);
let reservationEnabled = true;
const queue = kue.createQueue();
app.get('/available_seats', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }
  const job = queue.create('reserve_seat', {}).save(err => {
    if (!err) {
      return res.json({ status: 'Reservation in process' });
    }
    return res.json({ status: 'Reservation failed' });
  });
  job.on('complete', () => {
    console.log(`Notification job ${job.id} completed`);
  });
  job.on('failed', (err) => {
    console.log(`Notification job ${job.id} failed: ${err}`);
  });
});
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    const curr = await getCurrentAvailableSeats();
    const next = curr - 1;
    if (next < 0) {
      return done(new Error('Not enough seats available'));
    }
    await reserveSeat(next);
    if (next === 0) {
      reservationEnabled = false;
    }
    done();
  });
});
app.listen(1245);
});
