<template>
  <div class="container text-center">
    <div v-if="!gameOver">
      <div class="numbers mt-4">
        <span class="display-3">{{ leftNumber }}</span>
        <span class="display-3"> ? </span>
        <span class="display-3">{{ rightNumber }}</span>
      </div>
      <div class="d-flex justify-content-center mb-3">
        <button class="btn btn-primary mx-2" @click="checkAnswer('<')"><</button>
        <button class="btn btn-primary mx-2" @click="checkAnswer('=')">=</button>
        <button class="btn btn-primary mx-2" @click="checkAnswer('>')">></button>
      </div>
      <div class="my-2">Счет: {{ score }}</div>
      <div class="my-2">Осталось {{ time }} секунд</div>
    </div>
    <div v-else>
      <h2>Игра окончена, Счет: {{ score }}</h2>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      leftNumber: 0,
      rightNumber: 0,
      score: 0,
      time: 60,
      timer: null,
      gameOver: false,
      modifier: 3,
    };
  },
  methods: {
    generateNumbers() {
      this.leftNumber = Math.floor(Math.random() * this.modifier);
      this.rightNumber = Math.floor(Math.random() * this.modifier);
    },
    checkAnswer(selectedOperator) {
      let correctOperator;
      if (this.leftNumber < this.rightNumber) {
        correctOperator = '<';
      } else if (this.leftNumber > this.rightNumber) {
        correctOperator = '>';
      } else {
        correctOperator = '=';
      }

      if (selectedOperator == correctOperator) {
        this.score++;
        this.modifier *= 3; 
      } else {
        this.score -= 3;
      }

      this.generateNumbers(); 
    },
    startTimer() {
      this.timer = setInterval(() => {
        this.time--;
        if (this.time <= 0) {
          this.stopGame();
        }
      }, 1000);
    },
    stopGame() {
      this.gameOver = true;
      clearInterval(this.timer);
    },
  },
  mounted() {
    this.startTimer();
    this.generateNumbers();
  }
};
</script>