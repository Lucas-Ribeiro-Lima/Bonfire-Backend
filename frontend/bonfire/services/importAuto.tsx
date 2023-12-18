interface importAutoProp {
    file: File;
    option: string;
}

export async function importAuto({file, option}: importAutoProp) {
    return(
        // if (option === '1Instancia'){
        //         return;
        // }
        console.log(JSON.stringify({file, option}, null, 2))
    );
}