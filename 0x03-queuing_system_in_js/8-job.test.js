import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

describe('createPushNotificationsJobs', () => {
  let queue;
  before(() => {
    queue =  kue.createQueue();
    queue.testMode.enter();
  });
  after(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });
  it('should diasplay error if not arrary', () => {
    expect(() => createPushNotificationsJobs('not-an-array', queue)).to.throw(Error, 'Not an array');
  });
  it('should create 2 new jobs', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      }
    ];
    createPushNotificationsJobs((jobs, idx) => {
      expect(job.type).to.equal('push_notification_code_3');
      expect(job.date).to.deep.equal(job[idx]);
    });
  });
});
