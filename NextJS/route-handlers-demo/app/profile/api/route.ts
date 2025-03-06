import { type NextRequest } from "next/server";
import {headers,cookies} from "next/headers";

export async function GET(request:NextRequest){
    const requestHeaders = new Headers(request.headers);
    const headerList = headers();
    const theme = request.cookies.get("theme");
    (await cookies()).set("resultsPerPage","20");

    console.log(requestHeaders.get("Authorization"));
    console.log((await headerList).get("Authorization"));
    console.log(theme);
    console.log((await cookies()).get("resultsPerPage"))

    return new Response("<h1>Profile APi Data</h1>",{
        headers:{
            "Content-Type":"text/html",
            "Set-Cookie":"theme=dark",
        },
    });
}