<template>
  <div id="appp">
    <div class="navbarr">
        <RedButton />
    </div>
    <div id="app" class="app">
      <StartPage v-if="!isTesting && !isFinished" @start="startTest" />
      <TestPage
        v-if="isTesting"
        :currentExpression="currentExpression"
        :timeLeft="timeLeft"
        @answer="checkAnswer"
      />
      <ResultPage v-if="isFinished" :score="score" :expressions_answers="expressions_answers" :all_expressions="all_expressions" @reset="resetTest" />
    </div>
  </div>
</template>

<script>
import StartPage from "./StartPage.vue";
import TestPage from "./TestPage.vue";
import ResultPage from "./ResultPage.vue";
import axios from "axios";
import RedButton from "../../navbar/Return.vue";

export default {
  name: "App",
  components: {
    StartPage,
    TestPage,
    ResultPage,
    RedButton
  },
  data() {
    return {
      expressions: [], 
      currentExpression: "", 
      isTesting: false, 
      isFinished: false, 
      timeLeft: 60, 
      currentIndex: 0, 
      score: 0, 
      timer: null, 
      expressions_answers: [],
      all_expressions: 0,
      testId: 21
    };
  },
  methods: {
    generateExpressions() {
      const operators = [">", "<", "==="];
      this.expressions = Array.from({ length: 100 }, () => {
        const a = Math.floor(Math.random() * 50);
        const b = Math.floor(Math.random() * 50);
        const operator = operators[Math.floor(Math.random() * operators.length)];
        return `${a} ${operator} ${b}`;
      });
      //  this.expressions_answers = this.expressions
    },
    startTest() {
      this.generateExpressions();
      this.expressions_answers=[];
      this.currentIndex = 0;
      this.currentExpression = this.expressions[this.currentIndex];
      this.isTesting = true;
      this.isFinished = false;
      this.score = 0;
      this.timeLeft = 10;

      this.timer = setInterval(() => {
        this.timeLeft--;
        if (this.timeLeft <= 0) {
          this.endTest();
        }
      }, 1000);
    },
    checkAnswer(userAnswer) {
      if (this.currentIndex < this.expressions.length) {
        const correctAnswer = eval(this.currentExpression);
        if (userAnswer === correctAnswer) {
          this.score++;
          this.expressions_answers.push([this.currentExpression, true]);
        }
        else{
          this.expressions_answers.push([this.currentExpression, false]);
        }
        this.all_expressions++;
        this.nextExpression();
      }
    },
    nextExpression() {
      this.currentIndex++;
      if (this.currentIndex < this.expressions.length) {
        this.currentExpression = this.expressions[this.currentIndex];
      } else {
        this.currentExpression = "";
      }
    },
    endTest() {
      clearInterval(this.timer);
      this.isTesting = false;
      this.isFinished = true;
      this.saveTestResult();
    },
    resetTest() {
      this.isTesting = false;
      this.isFinished = false;
      this.timeLeft = 60;
      this.currentIndex = 0;
      this.score = 0;
      this.currentExpression = "";
      this.all_expressions = 0;
      
    },
    async saveTestResult() {
      const testResultData = {
        'user': localStorage.getItem('user_id'),
        "test": this.testId,
        "number_correct_answers": this.score,
        "number_all_answers": this.all_expressions,
        "complete_time": 10,
        "accuracy": this.score /this.all_expressions // Количество неправильных
      };
      console.log(testResultData);

      try {
        const response = await axios.post(
          'http://localhost:8000/api/test-results/create/',
          testResultData,
          {
            headers: { 'Content-Type': 'application/json' }
          }
        );
        console.log('Результат теста сохранен:', response.data);
      } catch (error) {
        console.error('Ошибка при сохранении результата:', error);
      }
    },
  },
};
</script>

<style scoped>
  #appp {
      height: 100vh;
      width: 100vw;
      display: grid;
      grid-template-rows: auto 1fr;
      justify-content: center;
      align-items: center; 
  }

.app {
  text-align: center;
  font-family: Arial, sans-serif;
  padding: 20px;

  /* height: 100vh; */
  display: flex;
  justify-content: center;
  flex-direction: column;
}
</style>