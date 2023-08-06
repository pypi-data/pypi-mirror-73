#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "comment_remover.h"


enum Mode
{
    none,
    single_quote,
    double_quote,
    regex,
    block_comment,
    line_comment,
    cond_comp
};


/**
 * @brief js_rem_comments - removes comments from JavaScript source code
 * @param src - the input source code
 *
 * @return comment removed source code, also: will insert new line character at
 *         the end if there isn't any.
 *         Should return NULL only in case of errors.
 */
char* js_rem_comments(const char* src)
{
    unsigned long long len;
    /* get length of input string and return NULL if it is empty */
    if (!(len = strlen(src)))
    {
        char* out_src = (char*) malloc(sizeof(char));
        out_src[0] = '\x0';
        return out_src;
    }

    /* the comment removed version of the input */
    char* in_src;
    bool need_nl;
    /* new line character already at the end */
    if (src[len - 1] == '\n')
    {
        /* allocate at least as much memory as the input needs +1 for the trailing \x0 character */
        in_src = (char*)malloc((len + 1)*sizeof(char));
        need_nl = false;
    }
    /* new line character will be inserted */
    else
    {
        /* allocate at least as much memory as the input needs +1 for the trailing \x0 character
           and +1 for the end line character */
        in_src = (char*)malloc((len + 2)*sizeof(char));
        need_nl = true;
    }

    /* memory allocation failed */
    if (!in_src)
        return NULL;


    /* new length depends on whether new line insertion was needed or not */
    unsigned long long nlen = need_nl ? len + 1 : len;
    /* insert null character at the end */
    in_src[nlen] = '\x0';

    /* current parsing mode */
    enum Mode mode = none;
    /* bytes copyed so far */
    unsigned long long bytes = 0;

    /* boundary checkings */
    if (len < 2)
    {
        if (need_nl) in_src[1] = '\n';
        return in_src;
    }
    if (len == 2 && (src[0] == '/' && (src[1] == '/' || src[1] == '*')))
    {
        char* out_src = (char*)realloc(in_src, sizeof(char));
        if (!out_src)
        {
            free(in_src);
            return NULL;
        }

        out_src[0] = '\x0';
        return out_src;
    }
    else
    {
        in_src[0] = src[0];
        in_src[1] = src[1];
        bytes += 2;

        if (src[0] == '"') mode = double_quote;
        if (src[0] == '\'') mode = single_quote;
        mode = (mode == double_quote) ^ (src[1] == '"') ? double_quote : none;
        mode = (mode == single_quote) ^ (src[1] == '\'') ? single_quote : none;

        if (src[0] == '/')
        {
            if (src[1] == '*')
            {
                if (src[2] == '@') mode = cond_comp;
                else
                { mode = block_comment; bytes -= 2; }
            }
            else if (src[1] == '/')
            { mode = line_comment; bytes -= 2; }
            else mode = regex;
        }
        else if (src[1] == '/')
        {
            if (src[2] == '*')
            {
                if (src[3] == '@') mode = cond_comp;
                else
                { mode = block_comment; bytes -= 2; }
            }
            else if (src[2] == '/')
            { mode = line_comment; bytes -= 2; }
            else mode = regex;
        }
    }

    for (unsigned long long i = 2; i < len; ++i)
    {
        switch (mode)
        {
        case (regex):
            if (src[i] == '/' && src[i - 1] != '/')
                mode = none;

            in_src[bytes++] = src[i];
            continue;
        case (single_quote):
            if (src[i] == '\'' && src[i - 1] != '\\')
                mode = none;

            in_src[bytes++] = src[i];
            continue;
        case (double_quote):
            if (src[i] == '"' && src[i - 1] != '\\')
                mode = none;

            in_src[bytes++] = src[i];
            continue;
        case (block_comment):
            if (src[i] == '*' && src[i + 1] == '/')
            {
                mode = none;
                ++i;
            }
            continue;
        case (line_comment):
            if (src[i + 1] == '\n' || src[i + 1] == '\r')
                mode = none;
            continue;
        case (cond_comp):
            if (src[i - 2] == '@' && src[i - 1] == '*' && src[i] == '/')
                mode = none;

            in_src[bytes++] = src[i];
            continue;
        default:
            in_src[bytes++] = src[i];
        }

        if (src[i] == '"') mode = double_quote;
        if (src[i] == '\'') mode = single_quote;

        if (src[i] == '/')
        {
            if (src[i + 1] == '*')
            {
                if (src[i + 2] == '@')
                {
                    mode = cond_comp;
                    in_src[bytes++] = src[i];
                }
                else
                { mode = block_comment; --bytes; }
            }
            else if (src[i + 1] == '/')
            { mode = line_comment; -- bytes; }
            else
            { mode = regex; }
        }
    }

    if (need_nl && bytes && in_src[bytes - 1] != '\n')
    {
        in_src[bytes] = '\n';
        ++bytes;
    }
    char* out_src = (char*)realloc(in_src, (bytes + 1)*sizeof(char));
    /* should be able to reallocate less than or equal to the original memory, but checking to be safe */
    if (!out_src)
    {
        free(in_src);
        return NULL;
    }

    out_src[bytes] = '\x0';


    return out_src;
}


int main()
{
    const char* filename = "D:/Users/skyzip/Documents/PyCharmProjects/deep_learn/seq2seq_attention_copy/repositories/hakimel/reveal.js/js/controllers/print.js";

    /* declare a file pointer */
    FILE* infile;
    char* buffer;
    unsigned long long numbytes;

    /* open an existing file for reading */
    /* quit if the file does not exist */
    if(fopen_s(&infile, filename, "r") != 0)
        return 1;

    /* Get the number of bytes */
    fseek(infile, 0L, SEEK_END);
    long test = ftell(infile);
    if (test < 0) return 1;
    numbytes = (unsigned long long)test + 1;

    /* reset the file position indicator to
    the beginning of the file */
    fseek(infile, 0L, SEEK_SET);

    /* grab sufficient memory for the
    buffer to hold the text */
    buffer = (char*)malloc(numbytes*sizeof(char));

    /* memory error */
    if(buffer == NULL)
        return 1;

    /* copy all the text into the buffer */
    unsigned long long bytes_read = fread(buffer, sizeof(char), numbytes, infile);
    buffer[bytes_read] = '\x0';
    fclose(infile);



    for (unsigned i = 0; i < 100000; ++i)
    {
        //printf("%s\n\n", buffer);
        char* removed = js_rem_comments(buffer);
        //printf("%s\n\n", removed);
        free(removed);
    }

    /* free the memory we used for the buffer */
    free(buffer);

    return 0;
}
