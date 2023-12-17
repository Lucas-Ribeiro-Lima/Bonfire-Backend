import { v4 as uuid } from 'uuid'

interface signInRequestData {
    username: string;
    password: string;
}

const delay = (amount = 1000) => new Promise(resolve => setTimeout(resolve, amount))


export default async function signInRequest({username, password}: signInRequestData){
    await delay()

    return {
        token: uuid(),
        user: {
            name: 'Lucas Ribeiro',
            email: 'lucasribeirolima974@gmail.com',
            avatar_url: 'https://github.com/Lucas-Ribeiro-Lima.png'
        }
    }
}