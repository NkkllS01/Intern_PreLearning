export default async function UsersPage(){
    const response = await fetch("https://jsonplaceholder.typicode.com/users");
    const users = await response.json();
    console.log(users);
    return (
        <h1>UsersPage</h1>
    )
}