<template>
    <div class="container">
        <div class="col-md-8 offset-md-2">
            <div class="btn-group" v-for="(tag, idx) in tags" :key="idx">
                <router-link
                    :to="{
                        name: 'questionsByTag',
                        params: { name: tag[0].name }
                    }"
                    class="btn btn-primary"
                    >{{ tag[0].name }} ({{ tag[1] }})</router-link
                >
            </div>
            <br />
            <br />
        </div>
    </div>
</template>

<script>
import axios from "axios"
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
            tags: []
        }
    },
    methods: {
        getTags() {
            const path = "/questions/categories"
            axios
                .get(path)
                .then((res) => {
                    this.tags = res.data.categories_tags
                })
                .catch((error) => {
                    console.error(error)
                })
        }
    },
    created() {
        this.getTags()
    }
})
</script>

<style scoped>
.btn-primary {
    margin-right: 5px;
}
</style>